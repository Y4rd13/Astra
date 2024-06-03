import keyboard
import time
import json
from datetime import datetime
from openai import OpenAI
from .stt import SpeechToText
from .tts import TextToSpeech
from .vision import Vision
from .typer import Typer

class Assistant:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        device_index = 3
        self.stt = SpeechToText(model_name="medium", device_index=device_index)  
        self.tts = TextToSpeech(api_key)
        self.vision = Vision()
        self.typer = Typer()
        self.vision.start()  # Iniciar captura continua en threads separados

    def ask_gpt(self, query):
        try:
            # Define el prompt para la función analyze_image y type_text
            request_params = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful multilingual and multimodal assistant called Astra. You can analyze images and answer questions about them, and you can type responses."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "functions": [
                    {
                        "name": "analyze_image",
                        "description": "Analyze the current screen or camera image",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "source": {
                                    "type": "string",
                                    "enum": ["screen", "camera"],
                                    "description": "The source of the image to analyze"
                                }
                            },
                            "required": ["source"]
                        }
                    },
                    {
                        "name": "type_text",
                        "description": "Type the provided text",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "text": {
                                    "type": "string",
                                    "description": "The text to type"
                                }
                            },
                            "required": ["text"]
                        }
                    }
                ]
            }

            start_time = time.time()
            response = self.client.chat.completions.create(**request_params)
            response_time = time.time() - start_time

            return response, response_time
        except Exception as e:
            print(f"Error al obtener respuesta de GPT-4o: {e}")
            return None, None

    def handle_function_call(self, function_call, command):
        function_name = function_call.name
        params = json.loads(function_call.arguments)
        
        if function_name == "analyze_image":
            self.handle_analyze_image(params, command)
        elif function_name == "type_text":
            self.handle_type_text(params)
        else:
            self.tts.speak("No puedo realizar esa acción.")

    def handle_analyze_image(self, params, command):
        source = params["source"]
        if source == "screen":
            image = self.vision.latest_screen_capture
        else:
            image = self.vision.latest_camera_capture
        query_from_image64 = self.vision.analyze_image(image, command)
        response_image, _ = self.ask_gpt(query_from_image64)
        description = response_image.choices[0].message.content
        self.tts.speak(description)

    def handle_type_text(self, params):
        text = params["text"]
        explanation = self.typer.type_code(text)
        if explanation:
            self.tts.speak(explanation)

    def process_command(self, command):
        response, response_time = self.ask_gpt(command)
        if response:
            message = response.choices[0].message
            print(f"Message: {message}")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'[{timestamp}][Mensaje: {command}] (Tiempo de respuesta: {response_time:.2f} segundos)')

            if message.function_call:
                self.handle_function_call(message.function_call, command)
            else:
                self.tts.speak(message.content)
                # Aquí añadimos la lógica para escribir el texto si es necesario
                if "```" in message.content:
                    print("Escribiendo código...")
                    explanation = self.typer.type_code(message.content)
                    if explanation:
                        self.tts.speak(explanation)

        else:
            self.tts.speak("Lo siento, hubo un error al procesar tu solicitud.")

    def start_recording(self):
        print("Grabación activada. Hable ahora.")
        command = self.stt.listen_for_activation().lower()
        print(f'Command: {command}')
        self.process_command(command)

    def run(self):
        print("Asistente Astra activado y listo para recibir comandos.")
        self.tts.speak("Hola, soy Astra. ¿En qué puedo ayudarte hoy?")
        
        keyboard.add_hotkey('ctrl+shift+a', self.start_recording)
        print("Presiona CTRL+SHIFT+A para comenzar a grabar.")
        try:
            keyboard.wait('esc')
        except KeyboardInterrupt:
            print("Goodbye!")

