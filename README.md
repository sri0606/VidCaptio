# VidCaptio

[![OpenAI Whisper](https://img.shields.io/badge/OpenAI-Whisper-blue)](https://openai.com)
[![ffmpeg](https://img.shields.io/badge/ffmpeg-latest-orange)](https://ffmpeg.org)
[![pywebview](https://img.shields.io/badge/pywebview-latest-yellow)](https://pywebview.flowrl.com/)
[![translators](https://img.shields.io/badge/translators-latest-green)](https://pypi.org/project/translators/)
[![PyTorch](https://img.shields.io/badge/PyTorch-latest-red)](https://pytorch.org/)


VidCaptio is a free and open-source video captioning software that enables users to add multi-language subtitles to their videos. It utilizes OpenAI's Whisper for speech recognition and ffmpeg for video processing. Additionally, it offers a graphical user interface (GUI) built using pywebview for easy navigation and operation.

## Features

- **Multi-Language Captioning**: VidCaptio allows users to add captions in multiple languages to their videos.
- **Flexible Captioning Options**: Users have the option to choose which languages they want to add captions for.
- **Speech Recognition**: Powered by OpenAI's Whisper, VidCaptio accurately transcribes speech from videos for captioning.
- **Edit captions**: You can aedit captions before applying them to the video.
- **Graphical User Interface (GUI)**: The simple GUI built with pywebview provides a user-friendly experience.

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
```bash
python -m vidcaptio_run
```


## Contributing

Contributions to VidCaptio are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License

VidCaptio is licensed under the GNU General Public License v3.0 (GPL-3.0). See [LICENSE](LICENSE) for more details.
