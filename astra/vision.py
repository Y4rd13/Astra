import threading
import cv2
import numpy as np
import base64
import logging
from PIL import ImageGrab
logger = logging.getLogger(__name__)

class Vision:
    def __init__(self):
        self.running = False
        self.screen_thread = threading.Thread(target=self.stream_screen, daemon=True)
        self.camera_thread = threading.Thread(target=self.stream_camera, daemon=True)
        self.latest_screen_capture = None
        self.latest_camera_capture = None

    def start(self):
        self.running = True
        self.screen_thread.start()
        self.camera_thread.start()

    def stop(self):
        self.running = False
        self.screen_thread.join()
        self.camera_thread.join()

    def stream_screen(self):
        logger.info("Starting screen stream...")
        while self.running:
            screen = ImageGrab.grab()
            screen_np = np.array(screen)  # Convert to a numpy array for processing
            self.latest_screen_capture = screen_np  # Save the latest capture

    def stream_camera(self):
        cap = cv2.VideoCapture(0)
        logger.info("Starting camera stream...")
        while self.running:
            ret, frame = cap.read()
            if ret:
                frame_np = np.array(frame)
                self.latest_camera_capture = frame_np  # Save the latest frame
        cap.release()

    def convert_to_base64(self, image_array):
        """Convert a numpy array image to base64 string for analysis."""
        _, buffer = cv2.imencode('.jpg', image_array)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        return image_base64

    def analyze_image(self, image_array, command):
        """Send the image to GPT-4o for a description."""
        logger.info("Analyzing image...")
        image_base64 = self.convert_to_base64(image_array)
        return [
            {"type": "text", "text": command},
            {"type": "image_url", "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}",
                "detail": "low"
                },
            }
        ]