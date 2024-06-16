import threading
from openai import OpenAI
from utils.audio_utils import play_sound
import pyaudio
import time
import logging
import numpy as np

logger = logging.getLogger(__name__)

chunk_size = 1024  # Asegurarse de que coincida con el de voice_visualizer

class TextToSpeech:
    def __init__(self, api_key, model="tts-1", voice="nova", visualizer=None):
        self.client = OpenAI(api_key=api_key)
        self.voice = voice
        self.model = model
        self.visualizer = visualizer
        logger.info(f"Model: {model} - Voice: {voice}")

    def speak(self, text):
        def play_text():
            play_sound("message-incoming.mp3")
            player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

            start_time = time.time()

            with self.client.audio.speech.with_streaming_response.create(
                model=self.model,
                voice=self.voice,
                response_format="pcm",
                input=text
            ) as response:
                logger.info(f"Time to first byte: {int((time.time() - start_time) * 1000)}ms")
                for chunk in response.iter_bytes(chunk_size=1024):
                    player_stream.write(chunk)
                    if self.visualizer:
                        # Convertir chunk a datos de numpy y actualizar el visualizador
                        data = np.frombuffer(chunk, dtype=np.int16) / 32768.0  # Normalizar
                        if len(data) < chunk_size:
                            data = np.pad(data, (0, chunk_size - len(data)), 'constant')
                        elif len(data) > chunk_size:
                            data = data[:chunk_size]
                        self.visualizer.update_plot(data)

            logger.info(f"Done in {int((time.time() - start_time) * 1000)}ms.")
            player_stream.close()

        # Run the play_text function in a separate thread
        threading.Thread(target=play_text).start()
