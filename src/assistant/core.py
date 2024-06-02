import keyboard
from openai import OpenAI
from .stt import SpeechToText
from .tts import TextToSpeech
from .vision import Vision

class Assistant:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        device_index = 3
        self.stt = SpeechToText(model_name="medium", device_index=device_index)  
        self.tts = TextToSpeech(api_key)
        self.vision = Vision()
        self.vision.start()  # Iniciar captura continua en threads separados

    def ask_gpt(self, query, tools=None, tool_choice="auto"):
        try:
            request_params = {
                "model": "gpt-4o",
                "messages": [
                    {
                    "role": "system", "content": "You are a helpful multilangual and multimodal assistant called Astra.",
                    "role": "user", "content": query
                    }
                ],
                # "temperature": .7,
            }

            if tools is not None:
                request_params["tools"] = tools
                request_params["tool_choice"] = tool_choice or "auto"

            response = self.client.chat.completions.create(**request_params)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error al obtener respuesta de GPT-4o: {e}")
            return "Lo siento, hubo un error al procesar tu solicitud."

    def run(self):
        print("Asistente Astra activado y listo para recibir comandos.")
        self.tts.speak("Hola, soy Astra. ¿En qué puedo ayudarte hoy?")

        def start_recording():
            print("Grabación activada. Hable ahora.")
            command = self.stt.listen_for_activation().lower()
            print(f'Command: {command}')

            if "apaga" in command:
                self.vision.stop()
                self.tts.speak("Apagando el asistente. ¡Hasta pronto!")
            elif "que ves en mi pantalla" in command or "que ves en mi camara" in command or "¿qué ves en mi pantalla?" in command or "¡que ves en mi pantalla!" in command:
                print('Analizando imagen...')
                image = self.vision.latest_screen_capture if "pantalla" in command else self.vision.latest_camera_capture
                description = self.vision.analyze_image(image, command)
                self.tts.speak(description)
            else:
                response = self.ask_gpt(command)
                self.tts.speak(response)

        # Start recording when CTRL+SHIFT+A is pressed
        keyboard.add_hotkey('ctrl+shift+a', start_recording)

        print("Presiona CTRL+SHIFT+A para comenzar a grabar.")
        try:
            keyboard.wait('esc')
        except KeyboardInterrupt:
            print("Goodbye!")