from openai import OpenAI
import numpy as np
import speech_recognition as sr
import whisper
import torch
import os
from dotenv import load_dotenv
import pyaudio
import time

load_dotenv()

# Configure device to use CUDA if available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize Whisper on the selected device
model = whisper.load_model("medium", device=device)

# Speech recognition configuration
recognizer = sr.Recognizer()

# OpenAI configuration
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Function to convert voice to text
def voice_to_text():
    with sr.Microphone(sample_rate=16000, device_index=3) as source:
        print("Please speak now...")
        audio = recognizer.listen(source)
        print("Recording finished, processing...")
        
        # Convert audio to text using Whisper
        audio_data = np.frombuffer(audio.get_wav_data(), np.int16).flatten().astype(np.float32) / 32768.0
        result = model.transcribe(audio_data)
        text = result['text']
        print(f"Recognized text: {text}")
        return text

# Function to get GPT-4 response
def get_gpt4_response(query):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": query},
        ],
        temperature=0.7,
        stream=True
    )
    collected_messages = []
    for chunk in response:
        chunk_message = chunk.choices[0].delta.content
        if chunk_message:
            collected_messages.append(chunk_message)
            print(chunk_message, end='', flush=True)
    response_text = ''.join(collected_messages)
    print(f"\nComplete response from GPT-4o: {response_text}")
    return response_text

def text_to_speech(text):
    player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    start_time = time.time()

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",
        response_format="pcm",
        input=text
    ) as response:
        print(f"Time to first byte: {int((time.time() - start_time) * 1000)}ms")
        for chunk in response.iter_bytes(chunk_size=1024):
            player_stream.write(chunk)

    print(f"Done in {int((time.time() - start_time) * 1000)}ms.")

# Main function
def main():
    user_text = voice_to_text()
    gpt4_response = get_gpt4_response(user_text)
    text_to_speech(gpt4_response)

if __name__ == "__main__":
    main()
