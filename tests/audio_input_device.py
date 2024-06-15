import sounddevice as sd
import numpy as np
import os

def list_audio_devices():
    print("Available input devices:")
    devices = sd.query_devices()
    for index, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            print(f"{index}: {device['name']}")

def monitor_input(device_index):
    try:
        def audio_callback(indata, frames, time, status):
            if status:
                print(status)
            volume_norm = np.linalg.norm(indata) * 10
            os.system("cls" if os.name == "nt" else "clear")  # Clears the console
            print("Monitoring... Press Ctrl+C to stop")
            print(f"{'#' * int(volume_norm)}")  # Simple volume visualization

        with sd.InputStream(device=int(device_index),
                            callback=audio_callback,
                            channels=1,
                            samplerate=44100):  # Ensure the sample rate is supported by the device
            while True:
                sd.sleep(1000)
    except Exception as e:
        print(f"Error opening audio device: {e}")

if __name__ == "__main__":
    list_audio_devices()
    device_index = input("Enter the index of the device to monitor: ")
    monitor_input(device_index)
