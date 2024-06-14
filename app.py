import tkinter as tk
import customtkinter as ctk
import os
from dotenv import load_dotenv
import queue
import threading
import sounddevice as sd
import numpy as np
from PIL import Image
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

from astra.core import Assistant
from utils.app_utils import center_window_to_display
from config.settings import Settings


class AstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Astra Assistant")
        self.root.geometry(center_window_to_display(self.root, 800, 600, self.root._get_window_scaling()))
        self.root.attributes('-alpha', 0.98)  # Set transparency to 98%

        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')

        # Create an instance of the assistant
        self.settings = Settings()
        self.astra = Assistant(api_key=api_key, device_index=self.settings.get_input_device(), ui_callback=self.append_message, settings=self.settings)

        # Create UI components
        self.create_widgets()
        self.audio_queue = queue.Queue()
        self.testing_audio = False
        self.audio_stream = None

    def create_widgets(self):
        # Configure grid layout for the root window to make it responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # Text area to display messages
        self.text_area = ctk.CTkTextbox(self.root, wrap=tk.WORD)
        self.text_area.grid(column=0, row=0, padx=20, pady=20, columnspan=3, sticky="nsew")

        # Text box for user input
        self.user_input = ctk.CTkTextbox(self.root, wrap=tk.WORD)
        self.user_input.grid(column=0, row=1, padx=20, pady=10, columnspan=3, sticky="nsew")

        # Load image for the send button
        self.image_send = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "assets", "img", "send.png")))

        # Button to send text
        self.send_button = ctk.CTkButton(self.root, text="", command=self.send_text, width=50, height=50, image=self.image_send, fg_color="transparent")
        self.send_button.grid(column=2, row=2, padx=20, pady=10)

        # Load images for the recording button
        self.image_record = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "assets", "img", "pause-play-00.png")))
        self.image_stop = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "assets", "img", "pause-play-01.png")))

        # Central button to record audio
        self.record_button = ctk.CTkButton(self.root, text="", command=self.toggle_recording, width=50, height=50, image=self.image_record, fg_color="transparent")
        self.record_button.grid(column=1, row=2, padx=20, pady=20)

        # Load image for the settings button
        self.image_settings = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "assets", "img", "settings.png")))

        # Button to open settings
        self.settings_button = ctk.CTkButton(self.root, text="", command=self.open_settings, width=50, height=50, image=self.image_settings, fg_color="transparent")
        self.settings_button.grid(column=0, row=2, padx=20, pady=10)

        # Variable to control recording
        self.recording = False

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.record_button.configure(image=self.image_stop)
        self.recording_thread = threading.Thread(target=self.record_and_process_audio)
        self.recording_thread.start()

    def stop_recording(self):
        self.recording = False
        self.record_button.configure(image=self.image_record)

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

    def send_text(self):
        text = self.user_input.get("1.0", tk.END).strip()
        if text:
            self.astra.process_command(text)

    def open_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry(center_window_to_display(settings_window, 600, 400, settings_window._get_window_scaling()))
        settings_window.attributes('-alpha', 0.98)
        
        # Make the settings window always on top
        settings_window.attributes("-topmost", True)
        # Ensure the settings window has focus
        settings_window.focus_force()

        tabview = ctk.CTkTabview(settings_window, width=580, height=360)
        tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        settings_window.grid_columnconfigure(0, weight=1)
        settings_window.grid_rowconfigure(0, weight=1)

        tab_sound = tabview.add("Sound Settings")
        tab_macros = tabview.add("Macros")
        tab_models = tabview.add("Models")

        self.create_sound_settings(tab_sound)
        self.create_macros_settings(tab_macros)
        self.create_models_settings(tab_models)

    def create_sound_settings(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(tab, text="Input Device:").grid(column=0, row=0, padx=10, pady=10, sticky="e")
        devices = sd.query_devices()
        input_devices = [f"{i}: {device['name']}" for i, device in enumerate(devices) if device['max_input_channels'] > 0]
        device_var = ctk.StringVar(value=self.settings.get_input_device())
        device_option_menu = ctk.CTkOptionMenu(tab, variable=device_var, values=input_devices)
        device_option_menu.grid(column=1, row=0, padx=10, pady=10, sticky="w")

        def save_sound_settings():
            selected_device_index = int(device_var.get().split(":")[0])
            self.settings.set_input_device(selected_device_index)

        ctk.CTkButton(tab, text="Save", command=save_sound_settings).grid(column=0, row=1, padx=10, pady=10, columnspan=2)
        
        self.progress_bar = ctk.CTkProgressBar(tab, width=300)
        self.progress_bar.grid(column=0, row=3, padx=10, pady=10, columnspan=2)
        self.progress_bar.set(0)
        
        self.test_button = ctk.CTkButton(tab, text="Test Input Device", command=lambda: self.toggle_test_input_device(int(device_var.get().split(":")[0])))
        self.test_button.grid(column=0, row=2, padx=10, pady=10, columnspan=2)

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
            self.progress_bar.set(volume_norm / 100)  # Update the progress bar based on volume

        try:
            with sd.InputStream(device=device_index, callback=audio_callback, channels=1, samplerate=44100) as stream:
                self.audio_stream = stream
                while self.testing_audio:
                    sd.sleep(100)
        except Exception as e:
            logger.error(f"Error opening audio device: {e}")

    def create_macros_settings(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(tab, text="Record Audio (play/stop):").grid(column=0, row=0, padx=10, pady=10, sticky="e")
        macro_var = ctk.StringVar(value=self.settings.get_macro())
        macro_entry = ctk.CTkEntry(tab, textvariable=macro_var)
        macro_entry.grid(column=1, row=0, padx=10, pady=10, sticky="w")

        def save_macros_settings():
            self.settings.set_macro(macro_var.get())

        ctk.CTkButton(tab, text="Save", command=save_macros_settings).grid(column=0, row=1, padx=10, pady=10, columnspan=2)

    def create_models_settings(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(tab, text="TTS Model:").grid(column=0, row=0, padx=10, pady=10, sticky="e")
        tts_model_var = ctk.StringVar(value=self.settings.get_tts_model())
        tts_model_option_menu = ctk.CTkOptionMenu(tab, variable=tts_model_var, values=["tts-1", "tts-1-hd"])
        tts_model_option_menu.grid(column=1, row=0, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(tab, text="TTS Voice:").grid(column=0, row=1, padx=10, pady=10, sticky="e")
        tts_voice_var = ctk.StringVar(value=self.settings.get_tts_voice())
        tts_voice_option_menu = ctk.CTkOptionMenu(tab, variable=tts_voice_var, values=["echo", "fable", "onyx", "nova", "shimmer"])
        tts_voice_option_menu.grid(column=1, row=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(tab, text="STT Model:").grid(column=0, row=2, padx=10, pady=10, sticky="e")
        stt_model_var = ctk.StringVar(value=self.settings.get_stt_model())
        stt_model_option_menu = ctk.CTkOptionMenu(tab, variable=stt_model_var, values=["tiny", "base", "small", "medium", "large"])
        stt_model_option_menu.grid(column=1, row=2, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(tab, text="AI Model:").grid(column=0, row=3, padx=10, pady=10, sticky="e")
        ai_model_label = ctk.CTkLabel(tab, text=self.settings.get_ai_model())
        ai_model_label.grid(column=1, row=3, padx=10, pady=10, sticky="w")

        def save_models_settings():
            self.settings.config["models"]["tts"]["model"] = tts_model_var.get()
            self.settings.config["models"]["tts"]["voice"] = tts_voice_var.get()
            self.settings.config["models"]["stt"]["model"] = stt_model_var.get()
            self.settings.save_config()

        ctk.CTkButton(tab, text="Save", command=save_models_settings).grid(column=0, row=4, padx=10, pady=10, columnspan=2)

    def append_message(self, sender, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.text_area.insert(tk.END, f"{timestamp} [{sender}]: {message}\n")
        self.text_area.yview(tk.END)

def main():
    root = ctk.CTk()
    ctk.set_appearance_mode("Dark")
    app = AstraApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()