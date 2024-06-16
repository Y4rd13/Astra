import tkinter as tk
import customtkinter as ctk
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

device_index = 3  # De acuerdo al input device que se utilice del micrófono
samplerate = 44100
chunk_size = 1024

class VoiceAnimationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Voice Animation")
        self.geometry("800x600")

        self.closing = False  # Variable de bandera para el estado de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Manejar evento de cierre

        self.figure, self.ax = plt.subplots()
        self.figure.patch.set_facecolor('black')  # Fondo negro para la figura
        self.ax.set_facecolor('black')  # Fondo negro para los ejes
        self.x = np.arange(0, chunk_size)
        self.line, = self.ax.plot(self.x, np.random.rand(chunk_size), color='cyan')  # Línea color cian
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlim(0, chunk_size)
        self.ax.spines['bottom'].set_color('white')  # Color blanco para los bordes
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')

        # Ocultar los ticks y las etiquetas
        self.ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.canvas.draw()

        self.stream = sd.InputStream(device=device_index,
                                     channels=1,
                                     samplerate=samplerate,
                                     blocksize=chunk_size,
                                     callback=self.audio_callback)
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        # Aseguramos que indata sea de la forma esperada
        if len(indata) == chunk_size and not self.closing:
            self.after(0, self.update_plot, indata)

    def update_plot(self, indata):
        if not self.closing:
            self.line.set_ydata(indata[:, 0])
            self.canvas.draw_idle()

    def on_closing(self):
        self.closing = True
        self.stream.stop()  # Detener el stream de audio
        self.stream.close()  # Cerrar el stream de audio
        self.destroy()  # Cerrar la ventana principal

if __name__ == "__main__":
    app = VoiceAnimationApp()
    app.mainloop()
