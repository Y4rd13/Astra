from PIL import Image as PILImage
import os
import threading
import pystray
from pystray import MenuItem as item

def create_tray_icon(self):
    image = PILImage.open(os.path.join(os.getcwd(), "assets", "img", "neuralgt-icon-round.png"))
    menu = (item('Open', self.show_main_window), item('Exit', self.exit_app))
    self.tray_icon = pystray.Icon("Astra Assistant", image, "Astra Assistant", menu)
    threading.Thread(target=self.tray_icon.run, daemon=True).start()

def show_main_window(self):
    self.on_restore(None)
    self.root.deiconify()
    self.root.state('normal')

def exit_app(self):
    self.tray_icon.stop()
    self.root.quit()
