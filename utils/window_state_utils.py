def on_minimize(self, event):
    if self.root.state() == "iconic":
        self.is_minimized = True
        self.overlay.deiconify()  # Show the overlay
        self.root.withdraw()  # Hide the main window

def on_restore(self, event):
    if self.is_minimized:
        self.is_minimized = False
        self.overlay.withdraw()  # Hide the overlay
        self.root.deiconify()  # Show the main window