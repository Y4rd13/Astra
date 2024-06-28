import logging
import os
import pygame
import threading
import numpy as np
import sounddevice as sd

logger = logging.getLogger(__name__)

pygame.mixer.init()  # Initialize pygame mixer once

def play_sound(sound_file: str):
    def play():
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sound_path = os.path.join(base_dir, 'assets', 'sounds', sound_file)

        try:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            logger.error(f"Error playing sound: {e}")

    threading.Thread(target=play).start()

def toggle_recording(self):
    if not self.recording:
        self.start_recording()
    else:
        self.stop_recording()

def start_recording(self):
    self.recording = True
    self.update_record_label(True)
    self.recording_thread = threading.Thread(target=self.record_and_process_audio)
    self.recording_thread.start()

def stop_recording(self):
    self.recording = False
    self.update_record_label(False)

def record_and_process_audio(self):
    while self.recording:
        command = self.astra.stt.listen_for_activation().lower()
        if command:
            self.audio_queue.put(command)
            break
    self.stop_recording()
    self.process_audio_queue()

def process_audio_queue(self):
    while not self.audio_queue.empty():
        command = self.audio_queue.get()
        self.astra.process_command(command)

def toggle_test_input_device(self, device_index):
    if not self.testing_audio:
        self.start_test_input_device(device_index)
    else:
        self.stop_test_input_device()

def start_test_input_device(self, device_index):
    self.testing_audio = True
    self.test_button.configure(text="Stop Test", fg_color="red")
    self.audio_test_thread = threading.Thread(target=self.test_input_device, args=(device_index,))
    self.audio_test_thread.start()

def stop_test_input_device(self):
    self.testing_audio = False
    self.test_button.configure(text="Test Input Device", fg_color="green")
    if self.audio_stream:
        self.audio_stream.stop()
        self.audio_stream.close()
    self.progress_bar.set(0)

def test_input_device(self, device_index):
    def audio_callback(indata, frames, time, status):
        if status:
            logger.info(f'Status: {status}')
        volume_norm = np.linalg.norm(indata) * 10
        self.progress_bar.set(volume_norm / 100)

    try:
        with sd.InputStream(device=device_index, callback=audio_callback, channels=1, samplerate=44100) as stream:
            self.audio_stream = stream
            while self.testing_audio:
                sd.sleep(50)
    except Exception as e:
        logger.error(f"Error opening audio device: {e}")
