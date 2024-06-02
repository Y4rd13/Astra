# assistant/vision.py
import threading
import cv2
import numpy as np
from PIL import ImageGrab
import base64
from io import BytesIO
from openai import OpenAI

client = OpenAI(api_key="sk-proj-HkBgxMimHa7rmeuAd8TuT3BlbkFJzlwAhiEaYG8Ma4I9JdHm")

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
            #print("Captura de pantalla actualizada.")

    def stream_camera(self):
        cap = cv2.VideoCapture(0)
        print("Iniciando cámara...")
        while self.running:
            ret, frame = cap.read()
            if ret:
                frame_np = np.array(frame)
                self.latest_camera_capture = frame_np  # Guardar el último frame
                #print("Captura de cámara actualizada.")
        cap.release()

    def convert_to_base64(self, image_array):
        """Convierte una imagen numpy array a base64 string para análisis."""
        image = cv2.imencode('.jpg', image_array)[1].tostring()
        image_base64 = base64.b64encode(image).decode('utf-8')
        return image_base64

    def analyze_image(self, image_array, question):
        """Envía la imagen a GPT-4o para obtener una descripción."""
        
        # Convert image to base64
        image_base64 = self.convert_to_base64(image_array)

        # Save image to file
        cv2.imwrite("image.jpg", image_array)

        # Send image to GPT-4o
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}",
                    "detail": "low"
                },
                },
            ],
            }
        ],
        max_tokens=300,
        )
        description = response.choices[0].message.content
        return description
