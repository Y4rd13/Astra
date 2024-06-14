import numpy as np
import speech_recognition as sr
import whisper
import torch
import logging

logger = logging.getLogger(__name__)

class SpeechToText:
    def __init__(self, model_name="medium", device_index=None):
        # Configuración de SpeechRecognizer
        self.recorder = sr.Recognizer()

        # Configuración del micrófono
        self.source = sr.Microphone(sample_rate=16000, device_index=device_index)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.audio_model = whisper.load_model(model_name, device=self.device)
        logger.info(f"Device Model: {self.audio_model.device} - Whisper Model: {model_name} - Device Index: {device_index}")

        with self.source as s:
            self.recorder.adjust_for_ambient_noise(s)

    def listen_for_activation(self):
        logger.info("Listening for activation...")
        with self.source as source:
            logger.info("Please speak now...")
            audio = self.recorder.listen(source)
            logger.info("Recording finished, processing...")

            # Convertir audio a texto usando Whisper
            audio_data = np.frombuffer(audio.get_wav_data(), np.int16).flatten().astype(np.float32) / 32768.0
            result = self.audio_model.transcribe(audio_data)
            text = result['text'].strip()
            logger.info(f"Recognized text: {text}")
            return text
