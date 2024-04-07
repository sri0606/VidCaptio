from asr import Transcriber
import subprocess
import os
from captions import Captioner
class Video():
    """
    
    """
    def __init__(self,media_path,language="en"):
        self.media_path = media_path
        if language == "en":
            model_path = "base.en"
        else:
            model_path = "large"

        self.language = language
            
        self.transcriber = Transcriber(model_path=model_path)

        self.captioner = Captioner(media_path=media_path)

    def get_transcript(self,min_char_length=35, max_char_length=45):
        """
        Generate transcript for the video

        Args:
            minimum_sentence_length (int, optional): The minimum number of words a sentence should have to be included in the output. Defaults to 5.
            max_sentence_length (int, optional): The maximum number of words a sentence should have to be included in the output. Defaults to 23.
        """
        return self.transcriber.get_transcript(self.media_path,min_char_length=min_char_length, max_char_length=max_char_length)
        
    def add_captions(self, dest_langs, caption_file_loc, captions_type):
        """
        Add captions to the video

        Args:
            transcript (dict): A dictionary containing the transcript of the video. The dictionary should have 'text' and 'segments' keys. 'text' is the full transcript of the video, and 'segments' is a list of dictionaries containing the start and end times and the text of each segment of the transcript.
        """
        transcript = self.get_transcript()

        self.captioner.generate_captions(transcript, srclan=self.language, languages=dest_langs, type=captions_type, captions_folder=caption_file_loc)

        # Use FFmpeg to add the captions to the video
        output_path = os.path.splitext(self.media_path)[0] + '_captioned.mp4'
        command = ['ffmpeg', '-i', self.media_path]

        for i, lang in enumerate(dest_langs):
            caption_file = os.path.join(caption_file_loc, f'{lang}.{captions_type}')
            if not os.path.isfile(caption_file):
                raise FileNotFoundError(f"The file {caption_file} does not exist or is not readable.")
            command.extend(['-i', caption_file])

        command.extend(['-map', '0'])

        for i in range(len(dest_langs)):
            command.extend(['-map', str(i+1)])

        command.extend(['-c', 'copy', '-c:s', 'mov_text'])

        for i, lang in enumerate(dest_langs):
            command.extend(['-metadata:s:s:' + str(i), f'language={lang}'])

            # Add more elif statements here for other languages

        command.append(output_path)
        subprocess.run(command)