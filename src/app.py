import tkinter as tk
import customtkinter as ctk
from assistant.core import Assistant
from dotenv import load_dotenv
import os
import threading
from config.settings import Settings
import sounddevice as sd
from datetime import datetime

class AstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Astra Assistant")
        self.root.geometry("800x600")

        load_dotenv()  # Carga las variables de entorno del archivo .env
        api_key = os.getenv('OPENAI_API_KEY')

        # Crear una instancia del asistente
        self.settings = Settings()
        self.astra = Assistant(api_key=api_key, device_index=self.settings.get_input_device())

        # Crear componentes de la UI
        self.create_widgets()

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
        self.text_area = ctk.CTkTextbox(self.root, width=600, height=400, wrap=tk.WORD)
        self.text_area.grid(column=0, row=0, padx=20, pady=20, columnspan=2)

        # Botón central para grabar audio
        self.record_button = ctk.CTkButton(self.root, text="Grabar", command=self.toggle_recording, width=200, height=50)
        self.record_button.grid(column=0, row=1, padx=20, pady=20, columnspan=2)

        # Variable para controlar la grabación
        self.recording = False

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.text_area.insert(tk.END, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [User]: Grabación activada. Hable ahora.\n")
        self.record_button.configure(text="Detener")
        self.recording_thread = threading.Thread(target=self.astra.start_recording)
        self.recording_thread.start()

    def stop_recording(self):
        self.recording = False
        self.text_area.insert(tk.END, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [User]: Grabación detenida.\n")
        self.record_button.configure(text="Grabar")
        # Aquí puedes agregar lógica para detener la grabación si es necesario

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

def main():
    root = ctk.CTk()
    ctk.set_appearance_mode("Dark")
    app = AstraApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
