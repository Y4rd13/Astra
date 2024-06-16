import tkinter as tk
import customtkinter as ctk
import os
from PIL import Image, ImageTk

def create_overlay(self):
    self.overlay = tk.Toplevel(self.root)
    self.overlay.geometry("100x100")
    self.overlay.overrideredirect(True)  # Remove window decorations
    self.overlay.attributes("-topmost", True)
    self.overlay.attributes('-alpha', 0.9)  # 10% transparent
    self.overlay.config(bg="black")

    # Set shape to be round
    self.overlay_canvas = tk.Canvas(self.overlay, width=100, height=100, bg="black", highlightthickness=0)
    self.overlay_canvas.pack(fill="both", expand=True)
    self.overlay_canvas.create_oval(0, 0, 100, 100, fill="black")

    # Create a frame inside the canvas to hold the button
    self.overlay_frame = ctk.CTkFrame(self.overlay, width=100, height=100, fg_color="black", corner_radius=50)
    self.overlay_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Load and resize images for the recording button in the overlay
    icon_path = os.path.join(os.getcwd(), "assets", "img", "icon.png")
    image_record = Image.open(icon_path)
    image_record_resized = image_record.resize((50, 50), Image.LANCZOS)
    self.overlay_image_record = ImageTk.PhotoImage(image_record_resized)
    
    icon_stop_path = os.path.join(os.getcwd(), "assets", "img", "pause-play-01.png")
    image_stop = Image.open(icon_stop_path)
    image_stop_resized = image_stop.resize((50, 50), Image.LANCZOS)
    self.overlay_image_stop = ImageTk.PhotoImage(image_stop_resized)

    # Central button to record audio in the overlay
    self.overlay_record_button = ctk.CTkButton(self.overlay_frame, text="", command=self.toggle_recording, width=50, height=50, image=self.overlay_image_record, fg_color="transparent")
    self.overlay_record_button.pack(expand=True)

    self.overlay.withdraw()  # Hide the overlay initially

    # Make overlay movable
    self.overlay.bind("<Button-1>", self.start_move)
    self.overlay.bind("<B1-Motion>", self.do_move)

def start_move(self, event):
    self.x = event.x
    self.y = event.y

def do_move(self, event):
    x = self.overlay.winfo_pointerx() - self.x
    y = self.overlay.winfo_pointery() - self.y
    self.overlay.geometry(f"+{x}+{y}")
