import logging
import os
import pygame
import threading

logger = logging.getLogger(__name__)

def play_sound(sound_file: str):
    def play():
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sound_path = os.path.join(base_dir, 'assets', 'sounds', sound_file)

        try:
            pygame.mixer.init()  # Ensure the mixer is initialized
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            
            # Wait until playback is finished
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Stop and quit the pygame mixer to free the file
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        except Exception as e:
            logger.error(f"Error playing incoming message sound: {e}")

    # Run the play function in a separate thread
    threading.Thread(target=play).start()
