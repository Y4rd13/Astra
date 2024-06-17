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
import pvporcupine
import pyaudio
import struct
from dotenv import load_dotenv 
load_dotenv()

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

        # Porcupine configuration
        keyword_path = os.path.join("models", "Astra_es_windows_v3_0_0.ppn")
        model_path = os.path.join("models", "porcupine_params_es.pv")
        self.porcupine = pvporcupine.create(access_key=os.getenv("PORCUPINE_ACCESS_KEY"), keyword_paths=[keyword_path], model_path=model_path)
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    async def load_model_async(self):
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            self.audio_model = await loop.run_in_executor(pool, self.load_model)
        logger.info(f"Device Model: {self.device} - Faster-Whisper Model: {self.model_size}")

    def load_model(self):
        return WhisperModel(self.model_size, device=self.device, compute_type="float16" if self.device == "cuda" else "int8")

    def listen_for_wake_word(self):
        logger.info("Listening for wake word...")
        while True:
            pcm = self.audio_stream.read(self.porcupine.frame_length)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

            keyword_index = self.porcupine.process(pcm)
            if keyword_index >= 0:
                logger.info("Wake word detected!")
                play_sound("wake-word-detected.mp3")
                self.listen_for_activation()
                break

    def listen_for_activation(self):
        if not self.audio_model:
            logger.error("Audio model is not loaded yet.")
            return ""

        logger.info("Listening for activation...")
        with self.source as source:
            logger.info("Please speak now...")
            audio = self.recorder.listen(source)
            logger.info("Recording finished, processing...")
            play_sound("wake-word-detected.mp3")

            # Convert audio to text using Faster-Whisper
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16).astype(np.float32) / 32768.0
            segments, info = self.audio_model.transcribe(audio_data, beam_size=5, vad_filter=True)
            
            text = " ".join(segment.text for segment in segments).strip()
            logger.info(f"Recognized text: {text}")
            return text
