
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

1. **Optimize STT**
   - [x] Optimize response time for STT processing.
  
2. **Core**
   - [x] Implement memory for the assistant to remember previous interactions.
   - [x] Limit memory/chat-history to a certain number of messages according to the token limit for the current model.
  
3. **STT**
   - [ ] Voice Activity Detection: Automatically detects when you start and stop speaking.
   - [ ] Wake Word Activation: Can activate upon detecting a designated wake word.
   - [x] Realtime Transcription: Transforms speech to text in real-time (fast-whisper).
   - [x] Integrate Faster-Whisper for faster STT processing.
  
4. **Vision**
   - [ ] semantic-chunking for video chunking analysis, instead of the current implementation.

5. **Audio Visualizer**:
   - [ ] Add a visualizer to display audio input levels (STT).
   - [x] Implement a visualizer for audio output (TTS).
   - [ ] Make the visualizer responsive.
   - [ ] Fix visualizer to generate sound across all the plot line.

6. **Fix `typer.py`**
   - [ ] Correct the indentation issue when writing code.
   - [ ] Ensure the generated code is properly formatted.
   - [ ] Verify that writing code in different languages maintains the appropriate indentation.

7. **UI**
   - [ ] Add switch button to keep active screen and/or cam vision.
   - [ ] Add a button to attach a file to the chat. (Image, audio, video, etc.)
   - [x] Make the chat box responsive to the window size.
   - [x] Add sound effects with threading to avoid blocking the UI.
   - [ ] Add a button to clear the chat history. 
   - [x] Add icons to the buttons.
   - [x] Make overlay widget.
   - [x] Add transparency
   - [x] Implement "design settings" to allow users to customize the UI (dark mode, light mode, adjust transparency, etc.)
   - [x] Adding Welcome Sound 
   - [x] Add new icons 
   - [ ] Stop/Record button can interrupt the assistant's response to give priority to the user's input.

8. **Fix Default Macro**
   - [ ] Ensure the `ctrl+shift+a` key combination works correctly.
   - [ ] Allow customization of the macro through the settings.
  
9.  **Essentials**:
   - Astra response time optimization
     - [x] General optimization: core (general methods) + stt (loading model) + tts (chunk processing)
     - [x] Improve response time for STT
     - [ ] Implement setting to adjust noise reduction for STT
     - [ ] Improve response time for the vision module

10. **Other**
   - [ ] Add more constants (images path, sounds path, etc) to `constants.py` to avoid hardcoding.
   - [ ] Implement LangChain for multiple languages as Agents for the assistant.
   - [ ] Implement local LLMs such as:
       - [ ] MistralAI
       - [ ] Codestral
       - [ ] Whisper fine-tuned models to hear Astra's name.
   - [ ] Implement function calling such as:
       - [ ] Astra stop 
  

### Notes

- [Window Icon in Tk (tkinter)](https://pythonassets.com/posts/window-icon-in-tk-tkinter/)