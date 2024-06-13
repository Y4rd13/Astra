import numpy as np
import speech_recognition as sr
import whisper
import torch
import logging
from queue import Queue
from datetime import datetime
from time import sleep
logger = logging.getLogger(__name__)

class SpeechToText:
    """
    Initialize the SpeechToText class with configuration for speech recognition and transcription.

    Parameters:
    ------------
    model_name : str, optional
        The size of the model to be used from the Whisper library (e.g., "tiny", "base", "small", "medium", "large").
        Default is "medium"; "large", which is larger and typically more accurate, but requires more computational power.

    device_index : int, optional
        The index of the microphone device to be used for audio input. If None, the default microphone is used.
        This allows selection of a specific microphone if multiple are available.

    energy_threshold : int, optional
        The energy level threshold for considering whether a segment of audio contains speech. Higher values
        make the recognizer less sensitive to quieter sounds. This helps in reducing false positives due to noise.

    record_timeout : int, optional
        Maximum number of seconds the recorder waits for speech before stopping. Helps to prevent too long
        periods of silence from being considered as part of speech input.

    phrase_timeout : int, optional
        Maximum number of seconds allowed for a pause within a speech before considering the speech as ended.
        This helps in splitting the input into logical chunks at pauses, improving overall transcription accuracy.

    Attributes:
    -----------
    data_queue : Queue
        Queue used to hold raw audio data chunks being processed.

    transcription : list of str
        List that accumulates transcriptions of detected speech.

    recorder : Recognizer
        Instance of the Recognizer class from the speech_recognition library, configured to specific energy thresholds.

    source : Microphone
        Microphone device configured to specified sample rate and device index.

    audio_model : whisper.Model
        Loaded Whisper model specified by model_name, set to run on GPU if available, otherwise CPU.

    """
    def __init__(self, model_name="medium", device_index=None, energy_threshold=1000, record_timeout=6, phrase_timeout=6):
        self.energy_threshold = energy_threshold
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout
        self.data_queue = Queue()
        self.transcription = ['']
        
        # SpeechRecognizer configuration
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = self.energy_threshold
        self.recorder.dynamic_energy_threshold = False
        
        # Microphone configuration
        self.source = sr.Microphone(sample_rate=16000, device_index=device_index)
        self.model = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.audio_model = whisper.load_model(self.model, device=self.device)
        logger.info(f"Device model: {self.audio_model.device}, model: {model_name}, device index: {device_index}")
        
        with self.source as s:
            self.recorder.adjust_for_ambient_noise(s)
        
        self.recorder.listen_in_background(self.source, self.record_callback, phrase_time_limit=self.record_timeout)

    def record_callback(self, recognizer, audio):
        data = audio.get_raw_data()
        self.data_queue.put(data)

    def listen_for_activation(self):
        logger.info("Listening for activation...")
        combined_audio = []
        phrase_start_time = None

        while True:
            now = datetime.utcnow()
            if not self.data_queue.empty():
                if phrase_start_time is None:
                    phrase_start_time = now

                audio_data = b''.join(self.data_queue.queue)
                self.data_queue.queue.clear()
                combined_audio.append(audio_data)

                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                # Check the length of the audio to ensure it is reasonable
                if len(audio_np) < 16000:  # Less than one second of audio
                    sleep(0.25)
                    continue

                if (now - phrase_start_time).total_seconds() >= self.phrase_timeout:
                    logger.info("If the phrase timeout is reached, process the combined audio")
                    audio_combined_np = np.frombuffer(b''.join(combined_audio), dtype=np.int16).astype(np.float32) / 32768.0
                    result = self.audio_model.transcribe(audio_combined_np, fp16=torch.cuda.is_available())
                    text = result['text'].strip()
                    
                    self.transcription.append(text)
                    return text
            else:
                sleep(0.25)
                if phrase_start_time and (datetime.utcnow() - phrase_start_time).total_seconds() >= self.phrase_timeout:
                    logger.info("Process the combined audio if the phrase timeout is reached")
                    audio_combined_np = np.frombuffer(b''.join(combined_audio), dtype=np.int16).astype(np.float32) / 32768.0
                    result = self.audio_model.transcribe(audio_combined_np, fp16=torch.cuda.is_available())
                    text = result['text'].strip()

                    self.transcription.append(text)
                    return text
