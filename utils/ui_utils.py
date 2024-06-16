import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import os
import threading
from PIL import Image
from utils.voice_visualizer import VoiceVisualizer

def create_widgets(self):
    # Configure grid layout for the root window to make it responsive
    self.root.grid_columnconfigure(0, weight=1)
    self.root.grid_columnconfigure(1, weight=2)  # Increase weight for the voice visualizer
    self.root.grid_columnconfigure(2, weight=1)
    self.root.grid_rowconfigure(0, weight=0)  # VoiceVisualizer row
    self.root.grid_rowconfigure(1, weight=1)  # Text area row
    self.root.grid_rowconfigure(2, weight=1)  # User input row
    self.root.grid_rowconfigure(3, weight=0)  # Buttons row

    # Use the existing voice visualizer instance
    self.voice_visualizer.grid(row=0, column=1, columnspan=1, sticky="nsew")

    # Text area to display messages
    self.text_area = ctk.CTkTextbox(self.root, wrap=tk.WORD)
    self.text_area.grid(column=0, row=1, padx=20, pady=20, columnspan=3, sticky="nsew")

    # Text box for user input
    self.user_input = ctk.CTkTextbox(self.root, wrap=tk.WORD)
    self.user_input.grid(column=0, row=2, padx=20, pady=10, columnspan=3, sticky="nsew")

    # Load image for the send button
    self.image_send = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "assets", "img", "send.png")))

    # Button to send text
    self.send_button = ctk.CTkButton(self.root, text="", command=self.send_text, width=50, height=50, image=self.image_send, fg_color="transparent")
    self.send_button.grid(column=2, row=3, padx=20, pady=10)

    # Load images for the recording button
    self.image_record = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "assets", "img", "pause-play-00.png")))
    self.image_stop = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "assets", "img", "pause-play-01.png")))

    # Central button to record audio
    self.record_button = ctk.CTkButton(self.root, text="", command=self.toggle_recording, width=50, height=50, image=self.image_record, fg_color="transparent")
    self.record_button.grid(column=1, row=3, padx=20, pady=20)

    # Load image for the settings button
    self.image_settings = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "assets", "img", "settings.png")))

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
