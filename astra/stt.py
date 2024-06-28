import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import numpy as np
import speech_recognition as sr
from faster_whisper import WhisperModel
import torch
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import pvporcupine
from pvrecorder import PvRecorder
from huggingface_hub import hf_hub_download
from utils.audio_utils import play_sound
from dotenv import load_dotenv 
load_dotenv()

logger = logging.getLogger(__name__)

class SpeechToText:
    def __init__(self, model_name="large-v3", device_index: int = 2):
        device_index = 1
        self.recorder = sr.Recognizer()
        self.source = sr.Microphone(sample_rate=16000, device_index=2)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.audio_model = None
        self.model_size = model_name
        asyncio.run(self.load_model_async())
        
        with self.source as s:
            self.recorder.adjust_for_ambient_noise(s)

        self.keyword_paths = [self.download_model_from_huggingface("Y4rd13/Astra_es_windows_v3_0_0.ppn", "Astra_es_windows_v3_0_0.ppn")]
        self.model_path = self.download_model_from_huggingface("Y4rd13/porcupine_params_es.pv", "porcupine_params_es.pv")
        self.porcupine = pvporcupine.create(
            access_key=os.getenv("PORCUPINE_ACCESS_KEY"),
            keyword_paths=self.keyword_paths,
            model_path=self.model_path
        )
        self.audio_recorder = PvRecorder(device_index=device_index, frame_length=self.porcupine.frame_length)
        self.audio_recorder.start()
        self.stop_listening = False


    async def load_model_async(self):
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            self.audio_model = await loop.run_in_executor(pool, self.load_model)
        logger.info(f"Device Model: {self.device} - Faster-Whisper Model: {self.model_size}")

    def load_model(self):
        return WhisperModel(self.model_size, device=self.device, compute_type="float16" if self.device == "cuda" else "int8")

    def download_model_from_huggingface(self, model_repo, filename):
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        model_file = hf_hub_download(repo_id=model_repo, filename=filename, use_auth_token=api_key)
        return model_file

    def listen_for_wake_word(self):
        logger.info("Listening for wake word...")
        try:
            while not self.stop_listening:
                pcm = self.audio_recorder.read()
                result = self.porcupine.process(pcm)
                if result >= 0:
                    play_sound("wake-word-detected.mp3")
                    logger.info("Wake word detected!")
                    command = self.listen_for_activation()
                    if command:
                        logger.info(f"Command detected: {command}")
                        return command
        except KeyboardInterrupt:
            logger.info("Stopping...")

    def listen_for_activation(self):
        if not self.audio_model:
            logger.error("Audio model is not loaded yet.")
            return ""

        logger.info("Listening for activation...")
        with self.source as source:
            logger.info("Please speak now...")
            audio = self.recorder.listen(source)
            logger.info("Recording finished, processing...")

            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16).astype(np.float32) / 32768.0
            segments, info = self.audio_model.transcribe(audio_data, beam_size=5, vad_filter=True)
            
            text = " ".join(segment.text for segment in segments).strip()
            logger.info(f"Recognized text: {text}")
            return text

    def stop(self):
        self.stop_listening = True
