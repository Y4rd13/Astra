import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import os
import threading
from PIL import Image
from utils.voice_visualizer import VoiceVisualizer

def create_widgets(self):
    image_size = (32, 32)

    # Configure grid layout for the root window to make it responsive
    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_columnconfigure(1, weight=2)  # Increase weight for the voice visualizer
    self.root.grid_columnconfigure(2, weight=1)
    self.root.grid_rowconfigure(0, weight=1)  # VoiceVisualizer row
    self.root.grid_rowconfigure(1, weight=1)  # Text area row
    self.root.grid_rowconfigure(2, weight=1)  # User input row
    self.root.grid_rowconfigure(3, weight=0)  # Buttons row

    # Use the existing voice visualizer instance
    self.voice_visualizer.grid(row=0, column=0, columnspan=3, sticky="nsew")

    # Text area to display messages
    self.text_area = ctk.CTkTextbox(self.root, wrap=tk.WORD)
    self.text_area.grid(column=0, row=1, padx=20, pady=20, columnspan=3, sticky="nsew")

    # Text box for user input
    self.user_input = ctk.CTkTextbox(self.root, wrap=tk.WORD)
    self.user_input.grid(column=0, row=2, padx=20, pady=10, columnspan=3, sticky="nsew")

    # Load and resize image for the send button
    send_image_path = os.path.join(os.getcwd(), "assets", "img", "send.png")
    send_image = Image.open(send_image_path)
    self.image_send = ctk.CTkImage(light_image=send_image, size=image_size)

    # Button to send text
    self.send_button = ctk.CTkButton(self.root, text="", command=self.send_text, width=50, height=50, image=self.image_send, fg_color="transparent")
    self.send_button.grid(column=2, row=3, padx=20, pady=10)

    # Load and resize images for the recording button
    record_image_path = os.path.join(os.getcwd(), "assets", "img", "pause-play-00.png")
    record_image = Image.open(record_image_path)
    self.image_record = ctk.CTkImage(light_image=record_image, size=image_size)

    stop_image_path = os.path.join(os.getcwd(), "assets", "img", "pause-play-01.png")
    stop_image = Image.open(stop_image_path)
    self.image_stop = ctk.CTkImage(light_image=stop_image, size=image_size)

    # Central button to record audio
    self.record_button = ctk.CTkButton(self.root, text="", command=self.toggle_recording, width=50, height=50, image=self.image_record, fg_color="transparent")
    self.record_button.grid(column=1, row=3, padx=20, pady=20)

    # Load and resize image for the settings button
    settings_image_path = os.path.join(os.getcwd(), "assets", "img", "settings.png")
    settings_image = Image.open(settings_image_path)
    self.image_settings = ctk.CTkImage(light_image=settings_image, size=image_size)

    # Button to open settings
    self.settings_button = ctk.CTkButton(self.root, text="", command=self.open_settings, width=50, height=50, image=self.image_settings, fg_color="transparent")
    self.settings_button.grid(column=0, row=3, padx=20, pady=10)

    # Variable to control recording
    self.recording = False

    # Create overlay window
    self.create_overlay()

def send_text(self):
    text = self.user_input.get("1.0", tk.END).strip()
    if text:
        self.astra.process_command(text)

def append_message(self, sender, message):
    def write_message():
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.text_area.insert(tk.END, f"{timestamp} [{sender}]: {message}\n")
        self.text_area.yview(tk.END)
    
    # Run write_message function in a separate thread
    threading.Thread(target=write_message).start()

def center_window_to_display(window, width, height, scale_factor=1.0):
    """Centers the window to the main display/monitor"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 1.5) - (height / 1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"