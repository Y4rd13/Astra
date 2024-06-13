import keyboard
import time
import json
from datetime import datetime
from openai import OpenAI
from .stt import SpeechToText
from .tts import TextToSpeech
from .vision import Vision
from .typer import Typer
from utils.constants import request_payload

class Assistant:
    def __init__(self, api_key, device_index, ui_callback=None, settings=None):
        self.client = OpenAI(api_key=api_key)
        self.ui_callback = ui_callback  # Callback to update the UI
        self.settings = settings
        self.stt = SpeechToText(model_name=self.settings.get_stt_model(), device_index=device_index)
        self.tts = TextToSpeech(api_key, model=self.settings.get_tts_model(), voice=self.settings.get_tts_voice())
        self.vision = Vision()
        self.typer = Typer()
        self.vision.start()  # Start continuous capture in separate threads

    def ask_gpt(self, query):
        try:
            # Define the prompt for the analyze_image and type_text functions
            request_params = request_payload(query)
            
            start_time = time.time()
            response = self.client.chat.completions.create(**request_params)
            response_time = time.time() - start_time

            return response, response_time
        except Exception as e:
            print(f"Error obtaining response from GPT-4o: {e}")
            return None, None

    def handle_function_call(self, function_call, command):
        function_name = function_call.name
        params = json.loads(function_call.arguments)

        if function_name == "analyze_image":
            self.handle_analyze_image(params, command)
        elif function_name == "type_text":
            self.handle_type_text(params)
        else:
            self.tts.speak("I can't perform that action.")
            self.update_ui("Astra", "I can't perform that action.")

    def handle_analyze_image(self, params, command):
        source = params["source"]
        if source == "screen":
            image = self.vision.latest_screen_capture
        else:
            image = self.vision.latest_camera_capture
        query_from_image64 = self.vision.analyze_image(image, command)
        response_image, _ = self.ask_gpt(query_from_image64)
        if response_image and response_image.choices[0].message.content:
            description = response_image.choices[0].message.content
            self.tts.speak(description)
            self.update_ui("Astra", description)
        else:
            self.tts.speak("Sorry, I couldn't analyze the image.")
            self.update_ui("Astra", "Sorry, I couldn't analyze the image.")

    def handle_type_text(self, params):
        text = params["text"]
        explanation = self.typer.type_code(text)
        if explanation:
            self.tts.speak(explanation)
            self.update_ui("Astra", explanation)

    def process_command(self, command):
        self.update_ui("User", command)
        response, response_time = self.ask_gpt(command)
        if response:
            message = response.choices[0].message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'[{timestamp}][Message: {command}] (Response time: {response_time:.2f} seconds)')

            if message.content:
                self.tts.speak(message.content)
                self.update_ui("Astra", message.content)
                if "```" in message.content:
                    explanation = self.typer.type_code(message.content)
                    if explanation:
                        self.tts.speak(explanation)
                        self.update_ui("Astra", explanation)
            elif message.function_call:
                self.handle_function_call(message.function_call, command)
            else:
                self.tts.speak("Sorry, I couldn't process your request.")
                self.update_ui("Astra", "Sorry, I couldn't process your request.")
        else:
            self.tts.speak("Sorry, there was an error processing your request.")
            self.update_ui("Astra", "Sorry, there was an error processing your request.")

    def start_recording(self):
        command = self.stt.listen_for_activation().lower()
        self.process_command(command)

    def update_ui(self, sender, message):
        if self.ui_callback:
            self.ui_callback(sender, message)

    def run(self):
        self.tts.speak("Hello, I'm Astra. How can I help you today?")
        keyboard.add_hotkey('ctrl+shift+a', self.start_recording)
        try:
            keyboard.wait('esc')
        except KeyboardInterrupt:
            print("Goodbye!")