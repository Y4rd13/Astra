import customtkinter as ctk
import os
from dotenv import load_dotenv
import queue
import logging
from PIL import Image, ImageTk
from utils.audio_utils import (
    toggle_recording, start_recording, stop_recording, record_and_process_audio,
    process_audio_queue, toggle_test_input_device, start_test_input_device,
    stop_test_input_device, test_input_device, play_sound
)
from utils.overlay_utils import create_overlay, start_move, do_move
from utils.window_state_utils import on_minimize, on_restore
from utils.settings_utils import open_settings, create_sound_settings, create_macros_settings, create_models_settings, create_appearance_settings
from utils.tray_utils import create_tray_icon, show_main_window, exit_app
from utils.ui_utils import create_widgets, send_text, append_message, center_window_to_display, VoiceVisualizer

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

from astra.core import Assistant
from config.settings import Settings

class AstraApp:
    def __init__(self, root):
        self.root = root
        self.settings = Settings()
        
        # Set appearance mode based on settings
        ctk.set_appearance_mode(self.settings.get_theme())
        
        self.root.title("Astra")
        self.root.geometry(center_window_to_display(self.root, width=800, height=900, scale_factor=self.root._get_window_scaling()))
        self.root.attributes('-alpha', self.settings.get_transparency())  # Set initial transparency

        icon_path = os.path.join(os.getcwd(), "assets", "img", "neuralgt-icon.png")
        icon_image = Image.open(icon_path)
        icon_image_large = ImageTk.PhotoImage(icon_image.resize((32, 32), Image.LANCZOS))
        icon_image_small = ImageTk.PhotoImage(icon_image.resize((16, 16), Image.LANCZOS))
        self.root.wm_iconbitmap(os.path.join(os.getcwd(), "assets", "img", "neuralgt-icon.ico"))
        self.root.iconphoto(False, icon_image_large, icon_image_small)

        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')

        # Create the voice visualizer
        self.voice_visualizer = VoiceVisualizer(self.root, height=200)
        
        # Create an instance of the assistant
        self.astra = Assistant(api_key=api_key, device_index=self.settings.get_input_device(), ui_callback=self.append_message, settings=self.settings, voice_visualizer=self.voice_visualizer)

        # Create UI components
        self.create_widgets()
        self.audio_queue = queue.Queue()
        self.testing_audio = False
        self.audio_stream = None

        # Track the minimized state
        self.is_minimized = False

        # Bind the window state event
        self.root.bind("<Unmap>", self.on_minimize)
        self.root.bind("<Map>", self.on_restore)

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Store after ids
        self.after_ids = []

        # Create system tray icon
        self.create_tray_icon()

        # Welcome sound
        play_sound("welcome.mp3")

    def on_closing(self):
        self.cancel_after_tasks()
        self.root.withdraw() 
        self.root.quit()
        self.root.destroy()

    def schedule_after(self, delay, callback):
        after_id = self.root.after(delay, callback)
        self.after_ids.append(after_id)
        return after_id

    def cancel_after_tasks(self):
        for after_id in self.after_ids:
            try:
                self.root.after_cancel(after_id)
            except Exception as e:
                logger.error(f"Error cancelling after task {after_id}: {e}")
        self.after_ids.clear()

    # Import methods from utils
    toggle_recording = toggle_recording
    start_recording = start_recording
    stop_recording = stop_recording
    record_and_process_audio = record_and_process_audio
    process_audio_queue = process_audio_queue
    toggle_test_input_device = toggle_test_input_device
    start_test_input_device = start_test_input_device
    stop_test_input_device = stop_test_input_device
    test_input_device = test_input_device

    create_overlay = create_overlay
    start_move = start_move
    do_move = do_move

    on_minimize = on_minimize
    on_restore = on_restore

    open_settings = open_settings
    create_sound_settings = create_sound_settings
    create_macros_settings = create_macros_settings
    create_models_settings = create_models_settings
    create_appearance_settings = create_appearance_settings

    create_tray_icon = create_tray_icon
    show_main_window = show_main_window
    exit_app = exit_app

    create_widgets = create_widgets
    send_text = send_text
    append_message = append_message

def main():
    root = ctk.CTk()
    app = AstraApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
