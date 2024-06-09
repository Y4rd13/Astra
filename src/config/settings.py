import json
import os

CONFIG_FILE = 'config.json'

class Settings:
    def __init__(self):
        self.config = {
            "sound": {
                "input_device": 2  # Default device index
            },
            "macros": {
                "record_audio": "ctrl+shift+a"  # Default macro
            },
            "models": {
                "tts": {
                    "model": "tts-1",
                    "voice": "nova"
                },
                "stt": {
                    "model": "medium"
                },
                "ai": "gpt-4o"
            }
        }
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                self.config = json.load(file)
    
    def save_config(self):
        with open(CONFIG_FILE, 'w') as file:
            json.dump(self.config, file, indent=4)

    def get_input_device(self):
        return self.config["sound"]["input_device"]
    
    def set_input_device(self, device_index):
        self.config["sound"]["input_device"] = device_index
        self.save_config()
    
    def get_macro(self):
        return self.config["macros"]["record_audio"]
    
    def set_macro(self, macro):
        self.config["macros"]["record_audio"] = macro
        self.save_config()
    
    def get_tts_model(self):
        return self.config["models"]["tts"]["model"]
    
    def get_tts_voice(self):
        return self.config["models"]["tts"]["voice"]
    
    def get_stt_model(self):
        return self.config["models"]["stt"]["model"]
    
    def get_ai_model(self):
        return self.config["models"]["ai"]

settings = Settings()
