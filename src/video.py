from src.asr import Transcriber
import subprocess
import os
import json
from src.captions import generate_captions as captions_generator

class Video():
    """
    
    """
    def __init__(self):
        # multi language transcriber, uses large model
        self.transcriber = None
        # just for english, uses base.en
        self.eng_transcriber = None

    def get_transcript(self,media_path,source_lang,min_char_length=60, max_char_length=100):
        """
        Generate transcript for the video

        Args:
            minimum_sentence_length (int, optional): The minimum number of words a sentence should have to be included in the output. Defaults to 5.
            max_sentence_length (int, optional): The maximum number of words a sentence should have to be included in the output. Defaults to 23.
        """
        if source_lang=="en":
            if self.eng_transcriber is None:
                self.eng_transcriber = Transcriber(model_path="base.en")
            return self.eng_transcriber.get_transcript(media_path,source_lang, min_char_length=min_char_length, max_char_length=max_char_length)
        else:
            if self.transcriber is None:
                self.transcriber = Transcriber(model_path="large")
            return self.transcriber.get_transcript(media_path, source_lang, min_char_length=min_char_length, max_char_length=max_char_length)
        
    def generate_captions(self,media_path,vid_folder, source_lang, dest_langs, captions_type="srt",save_to_json=True):
        """
        Add captions to the video
        """
        transcript_path = os.path.join(vid_folder, 'transcript.json')
        # generate captions on the origanl file
        if not os.path.exists(transcript_path):
            transcript = self.get_transcript(media_path,source_lang)
            if save_to_json:
                # Save the transcript to a JSON file
                with open(transcript_path, 'w') as f:
                    json.dump(transcript, f)

        captions_generator(srclan=source_lang, languages=dest_langs, type=captions_type, captions_folder=vid_folder)
    
    def add_captions(self, vid_folder, vid_extension, dest_langs, captions_type="srt"):
        """
        Add captions to the video
        """
        video_path = os.path.join(vid_folder, "video" + vid_extension)
        output_path = os.path.join(vid_folder, 'captioned' + vid_extension)

        command = ['ffmpeg', '-i', video_path]

        for i, lang in enumerate(dest_langs):
            caption_file = os.path.join(vid_folder, f'{lang}.{captions_type}')
            if not os.path.isfile(caption_file):
                raise FileNotFoundError(f"The file {caption_file} does not exist or is not readable.")
            command.extend(['-i', caption_file])

        command.extend(['-map', '0', '-map', '0:a'])  # Map the video and audio streams

        for i in range(len(dest_langs)):
            command.extend(['-map', str(i+1)+':0'])  # Map the subtitle streams

        command.extend(['-c', 'copy', '-c:s', 'mov_text'])

        for i, lang in enumerate(dest_langs):
            command.extend(['-metadata:s:' + str(i+3), f'language={lang}'])  # Set the language for each subtitle stream
            command.extend(['-metadata:s:' + str(i+3), f'title={lang.upper()}'])  # Set the title for each subtitle stream

        command.append(output_path)
        print('\n\n')
        print("dest langs",dest_langs)
        print(' '.join(command))
        print('\n\n')
        subprocess.run(command)