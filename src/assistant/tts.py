import os
from openai import OpenAI
import pygame
import tempfile
import logging
logger = logging.getLogger(__name__)

class TextToSpeech:
    def __init__(self, api_key, model="tts-1", voice="nova"):
        self.client = OpenAI(api_key=api_key)
        self.voice = voice
        self.model = model
        
        # Initialize pygame mixer
        pygame.mixer.init()

    def speak(self, text):
        # Generate spoken audio from text
        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            
            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                response.stream_to_file(temp_audio_file.name)
                temp_audio_path = temp_audio_file.name
            
            # Play the audio file using pygame
            pygame.mixer.init()  # Ensure the mixer is initialized
            pygame.mixer.music.load(temp_audio_path)
            pygame.mixer.music.play()
            
            # Wait until playback is finished
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Stop and quit the pygame mixer to free the file
            pygame.mixer.music.stop()
            pygame.mixer.quit()

            # Remove the temporary file after playback
            try:
                os.remove(temp_audio_path)
            except Exception as e:
                logger.error(f"Error trying to remove temp audio file {temp_audio_path}: {e}")
        except Exception as e:
            logger.error(f"Error while generating audio: {e}")