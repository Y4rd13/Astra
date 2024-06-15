
import customtkinter as ctk
import sounddevice as sd
from . import app_utils

def open_settings(self):
    settings_window = ctk.CTkToplevel(self.root)
    settings_window.title("Settings")
    settings_window.geometry(app_utils.center_window_to_display(settings_window, 600, 400, settings_window._get_window_scaling()))
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

