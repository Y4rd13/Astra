# assistant/tts.py
import os
from openai import OpenAI
from pathlib import Path

class TextToSpeech:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.voice = "nova"  # Puedes cambiar a cualquier otra voz disponible: echo, fable, onyx, nova, shimmer
        self.model = "tts-1"  # Usar tts-1 para calidad estándar o tts-1-hd para alta calidad

    def speak(self, text):
        # Generar audio hablado a partir de texto
        print(f"Generando audio para: {text}")
        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            # Guardar el archivo de audio en un lugar accesible
            speech_file_path = Path(__file__).parent / "speech.mp3"
            response.stream_to_file(speech_file_path)
            # Reproducir el archivo de audio
            os.system(f"start {speech_file_path}")  # Comando para Windows, ajustar según el sistema operativo
        except Exception as e:
            print(f"Error al generar el audio: {e}")
