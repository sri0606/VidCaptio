# VidCaptio

VidCaptio is a free and open-source video captioning software that enables users to add multi-language captions to their videos. It utilizes OpenAI's Whisper for speech recognition and understanding and ffmpeg for video processing. Additionally, it offers a graphical user interface (GUI) built using wxPython for easy navigation and operation.

## Features

- **Multi-Language Captioning**: VidCaptio allows users to add captions in multiple languages to their videos.
- **Flexible Captioning Options**: Users have the option to choose which languages they want to add captions for.
- **Speech Recognition**: Powered by OpenAI's Whisper, VidCaptio accurately transcribes speech from videos for captioning.
- **Video Processing**: Utilizing ffmpeg, VidCaptio efficiently processes videos for captioning, ensuring high-quality output.
- **Graphical User Interface (GUI)**: The GUI built with wxPython provides a user-friendly experience for easy navigation and operation.

## Installation

To install VidCaptio, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/sri0606/VideoCaptioner.git
   ```

2. Install dependencies:

   ```bash
   cd src
   pip install -r requirements.txt
   ```

## Versions
src: This version is intended for developers and includes the source code for VidCaptio.
gui: This version is meant for regular users and provides a pre-built graphical user interface (GUI) for easy installation and usage.

## Usage

1. Launch VidCaptio using the provided command.
2. Select the video file you want to add captions to.
3. Choose the languages for captioning.
4. Click "Start" to begin the captioning process.
5. Once completed, the captioned video will be saved in the specified location.

## Contributing

Contributions to VidCaptio are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License

VidCaptio is licensed under the GNU General Public License v3.0 (GPL-3.0). See [LICENSE](LICENSE) for more details.

## Acknowledgements

- [OpenAI's Whisper](https://openai.com)
- [ffmpeg](https://ffmpeg.org)
- [wxPython](https://www.wxpython.org)

