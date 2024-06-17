import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import numpy as np
import speech_recognition as sr
from faster_whisper import WhisperModel
import torch
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from utils.audio_utils import play_sound

logger = logging.getLogger(__name__)

class SpeechToText:
    def __init__(self, model_name="large-v3", device_index: int = 2):
        # SpeechRecognizer configuration
        self.recorder = sr.Recognizer()

        # Microphone configuration
        self.source = sr.Microphone(sample_rate=16000, device_index=device_index)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load model asynchronously
        self.audio_model = None
        self.model_size = model_name
        asyncio.run(self.load_model_async())
        
        # Adjust for ambient noise once during initialization
        with self.source as s:
            self.recorder.adjust_for_ambient_noise(s)

    async def load_model_async(self):
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            self.audio_model = await loop.run_in_executor(pool, self.load_model)
        logger.info(f"Device Model: {self.device} - Faster-Whisper Model: {self.model_size}")

    def load_model(self):
        return WhisperModel(self.model_size, device=self.device, compute_type="float16" if self.device == "cuda" else "int8")

    def listen_for_activation(self):
        if not self.audio_model:
            logger.error("Audio model is not loaded yet.")
            return ""

        logger.info("Listening for activation...")
        with self.source as source:
            logger.info("Please speak now...")
            audio = self.recorder.listen(source)
            logger.info("Recording finished, processing...")
            play_sound("record-finished.mp3")

            # Convert audio to text using Faster-Whisper
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16).astype(np.float32) / 32768.0
            segments, info = self.audio_model.transcribe(
                audio_data, 
                beam_size=5,
                vad_filter=True # The default behavior is conservative and only removes silence longer than 2 seconds
            )
            
            text = " ".join(segment.text for segment in segments).strip()
            logger.info(f"Recognized text: {text}")
            return text
