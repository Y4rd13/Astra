import json
import logging
import tiktoken
import threading
from openai import OpenAI
from .stt import SpeechToText
from .tts import TextToSpeech
from .vision import Vision
from .typer import Typer
from utils.constants import request_payload

logger = logging.getLogger(__name__)

class Assistant:
    def __init__(self, api_key, device_index, ui_callback=None, settings=None, voice_visualizer=None):
        self.client = OpenAI(api_key=api_key)
        self.ui_callback = ui_callback
        self.settings = settings or {}
        self.stt = SpeechToText(model_name=self.settings.get_stt_model(), device_index=device_index)
        self.tts = TextToSpeech(api_key, model=self.settings.get_tts_model(), voice=self.settings.get_tts_voice(), visualizer=voice_visualizer)
        self.vision = Vision()
        self.typer = Typer()
        self.vision.start()

        self.chat_history = []
        self.tokenizer = tiktoken.encoding_for_model("gpt-4o")
        self.start_listening()
    
    def start_listening(self):
        def listen_and_process():
            while True:
                command = self.stt.listen_for_wake_word()
                if command:
                    self.process_command(command)
        
        threading.Thread(target=listen_and_process, daemon=True).start()

    def stop_speaking(self):
        self.tts.stop()

    def ask_gpt(self, query):
        try:
            self.chat_history.append({"role": "user", "content": query})
            request_params = request_payload(query, self.chat_history)

            response = self.client.chat.completions.create(**request_params, stream=True)
            collected_messages = []
            function_call = None
            function_name = None
            function_args = ''

            for chunk in response:
                choice = chunk.choices[0].delta
                if choice.content:
                    collected_messages.append(choice.content)
                    print(choice.content, end='', flush=True)
                if choice.function_call:
                    if choice.function_call.name:
                        function_name = choice.function_call.name
                    if choice.function_call.arguments:
                        function_args += choice.function_call.arguments

            response_text = ''.join(collected_messages)
            logger.info(f"Complete response from GPT-4o: {response_text}")

            if function_name:
                function_call = {"name": function_name, "arguments": function_args}

            self.chat_history.append({"role": "assistant", "content": response_text})
            self._trim_chat_history()

            return response_text, function_call
        except Exception as e:
            logger.error(f"Error obtaining response from GPT-4: {e}")
            return None, None

    def _trim_chat_history(self):
        MAX_TOKENS = 128000
        current_tokens = sum(len(self.tokenizer.encode(message['content'])) for message in self.chat_history if isinstance(message['content'], str))
        logger.info(f"Current tokens: {current_tokens}")

        while current_tokens > MAX_TOKENS:
            removed_message = self.chat_history.pop(0)
            current_tokens -= len(self.tokenizer.encode(removed_message['content']))

    def handle_function_call(self, function_call, command):
        function_name = function_call['name']
        params = json.loads(function_call['arguments'])

        function_mapping = {
            "analyze_image": self.handle_analyze_image,
            "type_text": self.handle_type_text,
            "stop_speaking": self.handle_stop_speaking
        }

        handler = function_mapping.get(function_name)
        if handler:
            handler(params, command)
        else:
            self._handle_unknown_function()

    def handle_stop_speaking(self, params, command):
        self.stop_speaking()
        self.update_ui("Astra", "Speech stopped.")

    def handle_analyze_image(self, params, command):
        image_source = params.get("source")
        image = self._get_image_by_source(image_source)
        query_from_image64 = self.vision.analyze_image(image, command)
        response_image, function_call = self.ask_gpt(query_from_image64)

        if response_image:
            self.tts.speak(response_image)
            self.update_ui("Astra", response_image)
        else:
            self._handle_analysis_failure()

    def handle_type_text(self, params):
        text = params.get("text")
        explanation = self.typer.type_code(text)
        if explanation:
            self.update_ui("Astra", explanation)

    def process_command(self, command):
        self.update_ui("User", command)
        response, function_call = self.ask_gpt(command)
        logger.info(f'Response: {response} - Function Call: {function_call}')

        if response:
            if function_call:
                self.handle_function_call(function_call, command)
            else:
                self._process_message_content(response)
        else:
            if function_call:
                self.handle_function_call(function_call, command)
            else:
                self._handle_processing_failure()

    def update_ui(self, sender, message):
        if self.ui_callback:
            self.ui_callback(sender, message)

    def _get_image_by_source(self, source):
        return self.vision.latest_screen_capture if source == "screen" else self.vision.latest_camera_capture

    def _process_message_content(self, message):
        self.tts.speak(message)
        self.update_ui("Astra", message)
        if "```" in message:
            explanation = self.typer.type_code(message)
            if explanation:
                self.tts.speak(explanation)
                self.update_ui("Astra", explanation)

    def _handle_unknown_function(self):
        self.tts.speak("No puedo realizar esa acción.")
        self.update_ui("Astra", "No puedo realizar esa acción.")

    def _handle_analysis_failure(self):
        self.tts.speak("Lo siento, no pude analizar la imagen.")
        self.update_ui("Astra", "Lo siento, no pude analizar la imagen.")

    def _handle_processing_failure(self):
        self.tts.speak("Lo siento, hubo un error al procesar tu solicitud.")
        self.update_ui("Astra", "Lo siento, hubo un error al procesar tu solicitud.")
