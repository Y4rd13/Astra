import json
import os
import logging
logger = logging.getLogger(__name__)

CONFIG_FILE = 'config.json'

class Settings:
    def __init__(self):
        # Default settings
        self.config = {
            "sound": {
                "input_device": 2
            },
            "macros": {
                "record_audio": "ctrl+shift+a"
            },
            "models": {
                "tts": {
                    "model": "tts-1",
                    "voice": "nova"
                },
                "stt": {
                    "model": "large-v3"
                },
                "ai": "gpt-4o" 
            },
            "appearance": {
                "transparency": 0.98,
                "theme": "Dark"
            }
        }
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            logger.info("Loading config file...")
            with open(CONFIG_FILE, 'r') as file:
                self.config = json.load(file)
        else:
            logger.info("Config file not found, creating default config...")
            logger.info(os.path.abspath(CONFIG_FILE))
            self.save_config()
    
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

    def get_transparency(self):
        return self.config["appearance"]["transparency"]
    
    def set_transparency(self, transparency):
        self.config["appearance"]["transparency"] = transparency
        self.save_config()

    def get_theme(self):
        return self.config["appearance"]["theme"]
    
    def set_theme(self, theme):
        self.config["appearance"]["theme"] = theme
        self.save_config()

settings = Settings()
