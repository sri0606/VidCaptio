from asr import Transcriber
import subprocess
import os

class Video():
    """
    
    """
    def __init__(self,media_path):
        self.media_path = media_path
        self.transcriber = Transcriber(model_path="base.en")

    def add_captions(self,caption_file_loc="captions",captions_type="srt"):
        """
        Add captions to the video

        Args:
            transcript (dict): A dictionary containing the transcript of the video. The dictionary should have 'text' and 'segments' keys. 'text' is the full transcript of the video, and 'segments' is a list of dictionaries containing the start and end times and the text of each segment of the transcript.
        """
        print(os.path.abspath(f'{caption_file_loc}.{captions_type}'))
        self.transcriber.generate_caption_file(self.media_path,caption_file_loc)
        # Use FFmpeg to add the captions to the video
        output_path = os.path.splitext(self.media_path)[0] + '_captioned.mp4'
        if not os.path.isfile(f'{caption_file_loc}.{captions_type}'):
            raise FileNotFoundError(f"The file {caption_file_loc}.{captions_type} does not exist or is not readable.")
        subprocess.run(['ffmpeg', '-i', self.media_path, '-vf', f'subtitles={caption_file_loc}.{captions_type}', output_path])
