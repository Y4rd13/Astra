import threading
from openai import OpenAI
from utils.audio_utils import play_sound
import pyaudio
import time
import logging
import numpy as np

logger = logging.getLogger(__name__)

chunk_size = 1024  # Same as in voice_effect.py for the visualizer plot

class TextToSpeech:
    def __init__(self, api_key, model="tts-1", voice="nova", visualizer=None):
        self.client = OpenAI(api_key=api_key)
        self.voice = voice
        self.model = model
        self.visualizer = visualizer
        self.current_stop_event = None
        logger.info(f"Model: {model} - Voice: {voice}")

    def speak(self, text):
        if self.current_stop_event:
            self.current_stop_event.set()

        stop_event = threading.Event()
        self.current_stop_event = stop_event

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
                    if stop_event.is_set():
                        break
                    player_stream.write(chunk)
                    if self.visualizer:
                        # Convert chunk to numpy data and update the visualizer
                        data = np.frombuffer(chunk, dtype=np.int16) / 32768.0  # Normalize the data
                        if len(data) < chunk_size:
                            data = np.pad(data, (0, chunk_size - len(data)), 'constant')
                        elif len(data) > chunk_size:
                            data = data[:chunk_size]
                        self.visualizer.update_plot(data)

            logger.info(f"Done in {int((time.time() - start_time) * 1000)}ms.")
            player_stream.close()

        threading.Thread(target=play_text).start()

    def stop(self):
        if self.current_stop_event:
            self.current_stop_event.set()
