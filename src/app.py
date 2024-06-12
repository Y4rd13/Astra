import tkinter as tk
import customtkinter as ctk
from assistant.core import Assistant
from dotenv import load_dotenv
import os
import threading
from config.settings import Settings
import sounddevice as sd
import numpy as np
from datetime import datetime
from PIL import Image
import queue

class AstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Astra Assistant")
        self.root.geometry("800x600")

        load_dotenv()  # Carga las variables de entorno del archivo .env
        api_key = os.getenv('OPENAI_API_KEY')

        # Crear una instancia del asistente
        self.settings = Settings()
        self.astra = Assistant(api_key=api_key, device_index=self.settings.get_input_device(), ui_callback=self.append_message, settings=self.settings)

        # Crear componentes de la UI
        self.create_widgets()
        self.audio_queue = queue.Queue()
        self.testing_audio = False
        self.audio_stream = None

    def create_widgets(self):
        # Menú de configuración
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Sound Settings", command=self.open_sound_settings)
        settings_menu.add_command(label="Macros", command=self.open_macros_settings)
        settings_menu.add_command(label="Models", command=self.open_models_settings)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # Área de texto para mostrar mensajes
        self.text_area = ctk.CTkTextbox(self.root, width=600, height=200, wrap=tk.WORD)
        self.text_area.grid(column=0, row=0, padx=20, pady=20, columnspan=2)

        # Cuadro de texto para entrada del usuario
        self.user_input = ctk.CTkTextbox(self.root, width=600, height=200, wrap=tk.WORD)
        self.user_input.grid(column=0, row=1, padx=20, pady=10, columnspan=2)

        # Cargar imagen para el botón de envío
        self.image_send = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "src", "img", "send.png")))

        # Botón para enviar texto
        self.send_button = ctk.CTkButton(self.root, text="", command=self.send_text, width=50, height=50, image=self.image_send, fg_color="transparent")
        self.send_button.grid(column=1, row=2, padx=20, pady=10)

        # Cargar imágenes para el botón de grabación
        self.image_record = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "src", "img", "pause-play-00.png")))
        self.image_stop = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "src", "img", "pause-play-01.png")))

        # Botón central para grabar audio
        self.record_button = ctk.CTkButton(self.root, text="", command=self.toggle_recording, width=50, height=50, image=self.image_record, fg_color="transparent")
        self.record_button.grid(column=0, row=2, padx=20, pady=20)

        # Variable para controlar la grabación
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

    def open_sound_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Sound Settings")

        ctk.CTkLabel(settings_window, text="Input Device:").grid(column=0, row=0, padx=10, pady=10)
        devices = sd.query_devices()
        input_devices = [f"{i}: {device['name']}" for i, device in enumerate(devices) if device['max_input_channels'] > 0]
        device_var = ctk.StringVar(value=self.settings.get_input_device())
        device_option_menu = ctk.CTkOptionMenu(settings_window, variable=device_var, values=input_devices)
        device_option_menu.grid(column=1, row=0, padx=10, pady=10)

        def save_sound_settings():
            selected_device_index = int(device_var.get().split(":")[0])
            self.settings.set_input_device(selected_device_index)
            settings_window.destroy()

        ctk.CTkButton(settings_window, text="Save", command=save_sound_settings).grid(column=0, row=1, padx=10, pady=10, columnspan=2)
        
        # Barra de progreso para visualizar la entrada de audio
        self.progress_bar = ctk.CTkProgressBar(settings_window, width=300)
        self.progress_bar.grid(column=0, row=3, padx=10, pady=10, columnspan=2)
        self.progress_bar.set(0)
        
        self.test_button = ctk.CTkButton(settings_window, text="Test Input Device", command=lambda: self.toggle_test_input_device(int(device_var.get().split(":")[0])))
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
                print(status)
            volume_norm = np.linalg.norm(indata) * 10
            self.progress_bar.set(volume_norm / 100)  # Actualizar la barra de progreso en función del volumen

        try:
            with sd.InputStream(device=device_index, callback=audio_callback, channels=1, samplerate=44100) as stream:
                self.audio_stream = stream
                while self.testing_audio:
                    sd.sleep(100)
        except Exception as e:
            print(f"Error al abrir el dispositivo de audio: {e}")

    def open_macros_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Macros")

        ctk.CTkLabel(settings_window, text="Record Audio (play/stop):").grid(column=0, row=0, padx=10, pady=10)
        macro_var = ctk.StringVar(value=self.settings.get_macro())
        macro_entry = ctk.CTkEntry(settings_window, textvariable=macro_var)
        macro_entry.grid(column=1, row=0, padx=10, pady=10)

        def save_macros_settings():
            self.settings.set_macro(macro_var.get())
            settings_window.destroy()

        ctk.CTkButton(settings_window, text="Save", command=save_macros_settings).grid(column=0, row=1, padx=10, pady=10, columnspan=2)

    def open_models_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Models")

        # TTS Settings
        ctk.CTkLabel(settings_window, text="TTS Model:").grid(column=0, row=0, padx=10, pady=10)
        tts_model_var = ctk.StringVar(value=self.settings.get_tts_model())
        tts_model_option_menu = ctk.CTkOptionMenu(settings_window, variable=tts_model_var, values=["tts-1", "tts-1-hd"])
        tts_model_option_menu.grid(column=1, row=0, padx=10, pady=10)

        ctk.CTkLabel(settings_window, text="TTS Voice:").grid(column=0, row=1, padx=10, pady=10)
        tts_voice_var = ctk.StringVar(value=self.settings.get_tts_voice())
        tts_voice_option_menu = ctk.CTkOptionMenu(settings_window, variable=tts_voice_var, values=["echo", "fable", "onyx", "nova", "shimmer"])
        tts_voice_option_menu.grid(column=1, row=1, padx=10, pady=10)

        # STT Settings
        ctk.CTkLabel(settings_window, text="STT Model:").grid(column=0, row=2, padx=10, pady=10)
        stt_model_var = ctk.StringVar(value=self.settings.get_stt_model())
        stt_model_option_menu = ctk.CTkOptionMenu(settings_window, variable=stt_model_var, values=["tiny", "base", "small", "medium", "large"])
        stt_model_option_menu.grid(column=1, row=2, padx=10, pady=10)

        # AI Model (Estático)
        ctk.CTkLabel(settings_window, text="AI Model:").grid(column=0, row=3, padx=10, pady=10)
        ai_model_label = ctk.CTkLabel(settings_window, text=self.settings.get_ai_model())
        ai_model_label.grid(column=1, row=3, padx=10, pady=10)

        def save_models_settings():
            self.settings.config["models"]["tts"]["model"] = tts_model_var.get()
            self.settings.config["models"]["tts"]["voice"] = tts_voice_var.get()
            self.settings.config["models"]["stt"]["model"] = stt_model_var.get()
            self.settings.save_config()
            settings_window.destroy()

        ctk.CTkButton(settings_window, text="Save", command=save_models_settings).grid(column=0, row=4, padx=10, pady=10, columnspan=2)

    def append_message(self, sender, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.text_area.insert(tk.END, f"{timestamp} [{sender}]: {message}\n")
        self.text_area.yview(tk.END)  # Desplazar automáticamente al final del texto

def main():
    root = ctk.CTk()
    ctk.set_appearance_mode("Dark")
    app = AstraApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

