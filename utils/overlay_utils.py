import tkinter as tk
import customtkinter as ctk
import os
from PIL import Image

def create_overlay(self):
    self.overlay = tk.Toplevel(self.root)
    self.overlay.geometry("100x100")
    self.overlay.overrideredirect(True)  # Remove window decorations
    self.overlay.attributes("-topmost", True)
    self.overlay.attributes('-alpha', 0.9)  # 3% transparent
    self.overlay.config(bg="black")

    # Set shape to be round
    self.overlay_canvas = tk.Canvas(self.overlay, width=100, height=100, bg="black", highlightthickness=0)
    self.overlay_canvas.pack(fill="both", expand=True)
    self.overlay_canvas.create_oval(0, 0, 100, 100, fill="black")

    # Load images for the recording button in the overlay
    self.overlay_image_record = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "assets", "img", "pause-play-00.png")))
    self.overlay_image_stop = ctk.CTkImage(light_image=Image.open(os.path.join(os.getcwd(), "assets", "img", "pause-play-01.png")))

    # Central button to record audio in the overlay
    self.overlay_record_button = ctk.CTkButton(self.overlay_canvas, text="", command=self.toggle_recording, width=50, height=50, image=self.overlay_image_record, fg_color="transparent")
    self.overlay_record_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

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
