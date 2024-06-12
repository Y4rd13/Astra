import os
from openai import OpenAI
from pathlib import Path
from pydub import AudioSegment
import pygame
import tempfile

class TextToSpeech:
    def __init__(self, api_key, model="tts-1", voice="nova"):
        self.client = OpenAI(api_key=api_key)
        self.voice = voice
        self.model = model
        
        # Inicializar pygame mixer
        pygame.mixer.init()

    def speak(self, text):
        # Generar audio hablado a partir de texto
        print(f"Generando audio para: {text}")
        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            
            # Crear un archivo temporal para el audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                response.stream_to_file(temp_audio_file.name)
                temp_audio_path = temp_audio_file.name
            
            # Reproducir el archivo de audio usando pygame
            pygame.mixer.init()  # Asegúrate de que el mixer esté inicializado
            pygame.mixer.music.load(temp_audio_path)
            pygame.mixer.music.play()
            
            # Esperar hasta que termine la reproducción
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Detener y cerrar el mixer de pygame para liberar el archivo
            print("Playback finished")
            pygame.mixer.music.stop()
            print("Stopping mixer")
            pygame.mixer.quit()
            print("Mixer stopped")

            # Eliminar el archivo temporal después de la reproducción
            try:
                os.remove(temp_audio_path)
            except Exception as e:
                print(f"Error al eliminar el archivo temporal: {e}")
                print(f"Ruta del archivo temporal: {temp_audio_path}")
        except Exception as e:
            print(f"Error al generar el audio: {e}")
