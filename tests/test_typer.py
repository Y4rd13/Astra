import pyaudio
import numpy as np
import noisereduce as nr
import scipy.io.wavfile as wavfile

# Parámetros de grabación
FORMAT = pyaudio.paInt16  # formato de la muestra de audio
CHANNELS = 1  # número de canales (1 = mono, 2 = estéreo)
RATE = 44100  # frecuencia de muestreo (samples per second)
CHUNK = 1024  # tamaño del buffer de audio
RECORD_SECONDS = 5  # duración de la grabación en segundos
OUTPUT_FILENAME = "output.wav"  # archivo de salida

# Inicializar PyAudio
audio = pyaudio.PyAudio()

# Abrir el stream para grabación
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Grabando...")

# Leer datos del micrófono
frames = []

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(np.frombuffer(data, dtype=np.int16))

    print("Grabación finalizada.")

    # Detener y cerrar el stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Convertir los frames a un array numpy
    audio_data = np.hstack(frames)

    # Aplicar reducción de ruido
    reduced_noise = nr.reduce_noise(y=audio_data, sr=RATE)

    # Guardar el archivo de audio resultante
    wavfile.write(OUTPUT_FILENAME, RATE, reduced_noise.astype(np.int16))

    print(f"Archivo guardado como {OUTPUT_FILENAME}")