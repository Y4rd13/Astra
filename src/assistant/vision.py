import threading
import cv2
import numpy as np
from PIL import ImageGrab
import base64

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
        print("Iniciando captura de pantalla...")
        while self.running:
            screen = ImageGrab.grab()
            screen_np = np.array(screen)  # Convertir a un array numpy para procesamiento
            self.latest_screen_capture = screen_np  # Guardar la última captura

    def stream_camera(self):
        cap = cv2.VideoCapture(0)
        print("Iniciando cámara...")
        while self.running:
            ret, frame = cap.read()
            if ret:
                frame_np = np.array(frame)
                self.latest_camera_capture = frame_np  # Guardar el último frame
        cap.release()

    def convert_to_base64(self, image_array):
        """Convierte una imagen numpy array a base64 string para análisis."""
        _, buffer = cv2.imencode('.jpg', image_array)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        return image_base64

    def analyze_image(self, image_array, command):
        """Envía la imagen a GPT-4o para obtener una descripción."""
        print("Analizando imagen...")
        image_base64 = self.convert_to_base64(image_array)
        return  [
            {"type": "text", "text": command},
            {"type": "image_url", "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}",
                "detail": "low"
                },
            }
        ]