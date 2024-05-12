from src.asr import Transcriber
import subprocess
import os
import glob
from src.captions import generate_captions as captions_generator

class Video():
    """
    
    """
    def __init__(self):
        # multi language transcriber, uses large model
        self.transcriber = None
        # just for english, uses base.en
        self.eng_transcriber = None

    def get_transcript(self,media_path,source_lang,min_char_length=35, max_char_length=45):
        """
        Generate transcript for the video

        Args:
            minimum_sentence_length (int, optional): The minimum number of words a sentence should have to be included in the output. Defaults to 5.
            max_sentence_length (int, optional): The maximum number of words a sentence should have to be included in the output. Defaults to 23.
        """
        if source_lang=="en":
            if self.eng_transcriber is None:
                self.eng_transcriber = Transcriber(model_path="base.en")
            return self.eng_transcriber.get_transcript(media_path,min_char_length=min_char_length, max_char_length=max_char_length)
        else:
            if self.transcriber is None:
                self.transcriber = Transcriber(model_path="large")
            return self.transcriber.get_transcript(media_path,min_char_length=min_char_length, max_char_length=max_char_length)
        
    def generate_captions(self,media_path,vid_folder, source_lang, dest_langs, captions_type="srt"):
        """
        Add captions to the video
        """
        # generate captions on the origanl file
        transcript = self.get_transcript(media_path,source_lang)
        captions_generator(transcript, srclan=source_lang, languages=dest_langs, type=captions_type, captions_folder=vid_folder)
    
    def add_captions(self,vid_folder,vid_extension, dest_langs, captions_type="srt"):
        """
        Add captions to the video
        """
        video_path= os.path.join(vid_folder,"video"+vid_extension)
        output_path = os.path.join(vid_folder ,'captioned'+vid_extension)

        # Use FFmpeg to add the captions to the video
        command = ['ffmpeg', '-i', video_path]

        for i, lang in enumerate(dest_langs):
            caption_file = os.path.join(vid_folder, f'{lang}.{captions_type}')
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