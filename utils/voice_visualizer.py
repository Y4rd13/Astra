import tkinter as tk
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

chunk_size = 1024

class VoiceVisualizer(ctk.CTkFrame):
    def __init__(self, parent, height=200, width=800):  # Añadir parámetro de ancho
        super().__init__(parent, height=height, width=width)
        self.closing = False  # Variable de bandera para el estado de cierre

        self.figure, self.ax = plt.subplots(figsize=(width/100, height/100))  # Ajustar tamaño de la figura
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
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.canvas.draw()

    def update_plot(self, data):
        if not self.closing:
            # Ajustar el tamaño de los datos recibidos
            if len(data) < chunk_size:
                data = np.pad(data, (0, chunk_size - len(data)), 'constant')
            elif len(data) > chunk_size:
                data = data[:chunk_size]

            self.line.set_ydata(data)
            self.canvas.draw_idle()

    def on_closing(self):
        self.closing = True
