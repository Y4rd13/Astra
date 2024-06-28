
# Astra Assistant 🚀

Welcome to **Astra Assistant**, your personal AI-powered assistant designed to enhance productivity and streamline tasks with a sophisticated user interface and advanced audio-visual capabilities.

## Features ✨

- **Speech Recognition** 🎤: Utilize the latest models for accurate voice command processing.
- **Text-to-Speech** 🗣️: High-quality voice output using state-of-the-art TTS models.
- **Image Analysis** 🖼️: Analyze and interpret images directly within the app.
- **Macro Customization** ⌨️: Set up and customize macros to suit your workflow.
- **User-Friendly UI** 🖥️: Intuitive and responsive interface built with `customtkinter`.

## Getting Started 🏁

### Prerequisites 📋

- Python 3.8 or higher
- Required packages (install via `pip`):
  - `tkinter`
  - `customtkinter`
  - `dotenv`
  - `sounddevice`
  - `numpy`
  - `Pillow`
  - `logging`
  - `opencv-python`
  - `keyboard`
  - `speech_recognition`
  - `whisper`
  - `pygame`

### Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/Y4rd13/Astra.git
   cd Astra
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

### Running the Application ▶️

To start the application, run:
```bash
python app.py
```

## Usage 🚀

### Main Interface 🖥️

- **Text Area**: Displays messages from the assistant.
- **User Input Box**: Type your commands or questions here.
- **Send Button**: Click to send your text input.
- **Record Button**: Toggle audio recording to interact with the assistant via voice commands.
- **Settings Button**: Access and customize application settings.

### Settings ⚙️

Customize your experience by adjusting settings for:
- **Sound Input Device**: Choose and test your preferred microphone.
- **Macros**: Configure keyboard shortcuts for quick actions.
- **Models**: Select preferred TTS and STT models, and configure the AI model used by the assistant.

## Development 🛠️

### Code Structure 📁

- **app.py**: Main application logic and UI setup.
- **settings.py**: Configuration management for user settings.
- **core.py**: Core functionality for handling commands and interactions.
- **stt.py**: Speech-to-text processing.
- **tts.py**: Text-to-speech synthesis.
- **typer.py**: Automated text typing and code parsing.
- **vision.py**: Image capture and analysis.

### Logging 📜

- Logging is configured to provide detailed runtime information.
- Logs are displayed in the console with timestamps for easy debugging.

## Contributing 🤝

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements 🙌

Special thanks to the contributors and the open-source community for their invaluable support and tools.

Enjoy using **Astra Assistant**! If you encounter any issues, feel free to open an [issue](https://github.com/Y4rd13/Astra/issues) on GitHub.

---
---
## TODO

1. **Core**
   - [x] Implement memory for the assistant to remember previous interactions.
   - [x] Limit memory/chat-history to a certain number of messages according to the token limit for the current model.
   - [ ] Implement LangChain for multiple languages as Agents for the assistant.
   - [ ] Implement local LLMs such as:
       - [ ] MistralAI
       - [ ] Codestral
       - [ ] Whisper fine-tuned models to hear Astra's name.
  
2. **STT**
   - [x] Optimize response time for STT processing.
   - [x] Voice Activity Detection: Automatically detects when you start and stop speaking.
   - [x] Always listening: Enable the assistant to listen continuously for voice commands.
   - [x] Wake Word Activation: Can activate upon detecting a designated wake word.
   - [x] Realtime Transcription: Transforms speech to text in real-time (fast-whisper).
   - [x] Integrate Faster-Whisper for faster STT processing.
   - [x] vad_filter integration: Enable the voice activity detection (VAD) to filter out parts of the audio without speech. This step is using the [Silero VAD model](https://github.com/snakers4/silero-vad).
   - [x] Implement function calling to stop the audio (i.e. Astra stop).
   - [x] New user's input will be priority over the current audio input. 
   - [x] Loading async `Astra_es_windows_v3_0_0.ppn` and `porcupine_params_es.pv` from Hugging Face.
   - [ ] Update input audio device settings to allow users to select the desired microphone.

3. **Vision**
   - [ ] semantic-chunking for video chunking analysis, instead of the current implementation.

4. **Fix `typer.py`**
   - [ ] Correct the indentation issue when writing code.
   - [ ] Ensure the generated code is properly formatted.
   - [ ] Verify that writing code in different languages maintains the appropriate indentation.

5. **Audio Visualizer**:
   - [ ] Add a visualizer to display audio input levels (STT).
   - [x] Implement a visualizer for audio output (TTS).
   - [ ] Make the visualizer responsive.
   - [ ] Fix visualizer to generate sound across all the plot line.

6. **UI**
   - [ ] Add switch button to keep active screen and/or cam vision.
   - [ ] Add a button to attach a file to the chat. (Image, audio, video, etc.)
   - [ ] Add a button to clear the chat history.
   - [x] Make the chat box responsive to the window size.
   - [x] Add sound effects with threading to avoid blocking the UI.
   - [x] Add icons to the buttons.
   - [x] Make overlay widget.
   - [x] Add transparency
   - [x] Implement "design settings" to allow users to customize the UI (dark mode, light mode, adjust transparency, etc.)
   - [x] Adding Welcome Sound 
   - [x] Add new icons 

7. **Fix Default Macro**
   - [ ] Ensure the `ctrl+shift+a` key combination works correctly.
   - [ ] Allow customization of the macro through the settings.
  
8.  **Essentials**:
   - Astra response time optimization
     - [x] General optimization: core (general methods) + stt (loading model) + tts (chunk processing)
     - [x] Improve response time for STT
     - [ ] Implement setting to adjust noise reduction for STT
     - [ ] Improve response time for the vision module

9.   **Other**
   - [ ] Add more constants (images path, sounds path, etc) to `constants.py` to avoid hardcoding.
  

### Notes

- [Window Icon in Tk (tkinter)](https://pythonassets.com/posts/window-icon-in-tk-tkinter/)

La imagen de record_image_path y stop_image_path en realidad no estan fucionando correctamente, la idea es la siguiente:
1. Por defecto la imagen utiliza `neuralgt-icon.png`
2. Cuando el usuario dice el wake word, entonces la imagen cambia a `neuralgt-icon-active.png`
3. Cuando el usuario deja de hablar, la imagen cambia a `neuralgt-icon.png`

En resumen:
1. La imagen por defecto es `neuralgt-icon.png`, que tambien indica que no se ha dicho el wake word, o que el proceso del STT ha finalizado (el usuario ya no esta hablando, obviamente luego de decir el wake word).
2. Cuando se detecta el wake word y luego el usuario esta hablando, `neuralgt-icon-active.png` actua como un indicador para el usuario de que ha dicho el wake word y que su audio esta siendo "escuchado" procesado por el STT.

por defecto -> `neuralgt-icon.png` -> luego usuario dice el wake word y empieza a hablar -> `neuralgt-icon-active.png` -> el usuario ha dejado de hablar -> vuelta al estado por defecto -> `neuralgt-icon.png`
