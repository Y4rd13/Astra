import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

chunk_size = 1024

class VoiceVisualizer(ctk.CTkFrame):
    def __init__(self, parent, height=100, width=800):
        super().__init__(parent, height=height, width=width)
        self.closing = False

        self.figure, self.ax = plt.subplots(figsize=(width/100, height/100))
        self.figure.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.x = np.arange(0, chunk_size)
        self.line, = self.ax.plot(self.x, np.zeros(chunk_size), color='cyan')
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlim(0, chunk_size)
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        self.ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.canvas.draw()

        self.bind("<Configure>", self.on_resize)

    def update_plot(self, data):
        if not self.closing:
            if len(data) < chunk_size:
                data = np.pad(data, (0, chunk_size - len(data)), 'constant')
            elif len(data) > chunk_size:
                data = data[:chunk_size]
            self.line.set_ydata(data)
            self.canvas.draw_idle()

    def on_resize(self, event):
        self.figure.set_size_inches(event.width / 100, event.height / 100)
        self.canvas.draw_idle()
