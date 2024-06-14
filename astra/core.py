import json
import logging
from openai import OpenAI
from .stt import SpeechToText
from .tts import TextToSpeech
from .vision import Vision
from .typer import Typer
from utils.constants import request_payload

logger = logging.getLogger(__name__)

class Assistant:
    def __init__(self, api_key, device_index, ui_callback=None, settings=None):
        self.client = OpenAI(api_key=api_key)
        self.ui_callback = ui_callback  # Callback to update the UI
        self.settings = settings or {}
        self.stt = SpeechToText(model_name=self.settings.get_stt_model(), device_index=device_index)
        self.tts = TextToSpeech(api_key, model=self.settings.get_tts_model(), voice=self.settings.get_tts_voice())
        self.vision = Vision()
        self.typer = Typer()
        self.vision.start()  # Start continuous capture in separate threads

    def ask_gpt(self, query):
        try:
            request_params = request_payload(query)
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
                function_call = {
                    "name": function_name,
                    "arguments": function_args
                }
            return response_text, function_call
        except Exception as e:
            logger.error(f"Error obtaining response from GPT-4: {e}")
            return None, None

    def handle_function_call(self, function_call, command):
        function_name = function_call['name']
        params = json.loads(function_call['arguments'])

        function_mapping = {
            "analyze_image": self.handle_analyze_image,
            "type_text": self.handle_type_text
        }

        handler = function_mapping.get(function_name)
        if handler:
            handler(params, command)
        else:
            self._handle_unknown_function()

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
            self.tts.speak(explanation)
            self.update_ui("Astra", explanation)

    def process_command(self, command):
        self.update_ui("User", command)
        response, function_call = self.ask_gpt(command)

        if response:
            if function_call:
                self.handle_function_call(function_call, command)
            else:
                self._process_message_content(response)
        else:
            self._handle_processing_failure()

    def start_recording(self):
        command = self.stt.listen_for_activation().lower()
        self.process_command(command)

    def update_ui(self, sender, message):
        if self.ui_callback:
            self.ui_callback(sender, message)

    def _get_image_by_source(self, source):
        if source == "screen":
            return self.vision.latest_screen_capture
        else:
            return self.vision.latest_camera_capture

    def _process_message_content(self, message):
        self.tts.speak(message)
        self.update_ui("Astra", message)
        if "```" in message:
            explanation = self.typer.type_code(message)
            if explanation:
                self.tts.speak(explanation)
                self.update_ui("Astra", explanation)

    def _handle_unknown_function(self):
        self.tts.speak("I can't perform that action.")
        self.update_ui("Astra", "I can't perform that action.")

    def _handle_analysis_failure(self):
        self.tts.speak("Sorry, I couldn't analyze the image.")
        self.update_ui("Astra", "Sorry, I couldn't analyze the image.")

    def _handle_processing_failure(self):
        self.tts.speak("Sorry, there was an error processing your request.")
        self.update_ui("Astra", "Sorry, there was an error processing your request.")
