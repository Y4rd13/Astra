import tkinter as tk
from tkinter import scrolledtext
from assistant.core import Assistant
from dotenv import load_dotenv
import os
import threading

class AstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Astra Assistant")
        
        load_dotenv()  # Carga las variables de entorno del archivo .env
        api_key = os.getenv('OPENAI_API_KEY')

        # Crear una instancia del asistente
        self.astra = Assistant(api_key=api_key)

        # Crear componentes de la UI
        self.create_widgets()

    def create_widgets(self):
        # Área de texto para mostrar mensajes
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.text_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        # Botón para iniciar la grabación
        self.record_button = tk.Button(self.root, text="Iniciar Grabación", command=self.start_recording)
        self.record_button.grid(column=0, row=1, padx=10, pady=10)

        # Botón para detener la grabación
        self.stop_button = tk.Button(self.root, text="Detener Grabación", command=self.stop_recording)
        self.stop_button.grid(column=1, row=1, padx=10, pady=10)

        # Botón para salir
        self.quit_button = tk.Button(self.root, text="Salir", command=self.root.quit)
        self.quit_button.grid(column=0, row=2, padx=10, pady=10, columnspan=2)

    def start_recording(self):
        self.text_area.insert(tk.END, "Grabación activada. Hable ahora.\n")
        self.recording_thread = threading.Thread(target=self.astra.start_recording)
        self.recording_thread.start()

    def stop_recording(self):
        self.text_area.insert(tk.END, "Grabación detenida.\n")
        # Aquí puedes agregar lógica para detener la grabación si es necesario

def main():
    root = tk.Tk()
    app = AstraApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
