from openai import OpenAI
from utils.audio_utils import play_sound
import pyaudio
import time
import logging
logger = logging.getLogger(__name__)

class TextToSpeech:
    def __init__(self, api_key, model="tts-1", voice="nova"):
        self.client = OpenAI(api_key=api_key)
        self.voice = voice
        self.model = model
        logger.info(f"Model: {model} - Voice: {voice}")

    def speak(self, text):
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

        logger.info(f"Done in {int((time.time() - start_time) * 1000)}ms.")
        player_stream.close()