import os
import json
from src.video import Video
from src.captions import parse_captions

class VidCaptioAPI:
    def __init__(self):
        self.video_captioner = Video()
        self.are_captions_generated = False
        self.captions_type="srt"

    def update_json_file(self, new_data):
        json_file_path = os.path.join(self.vid_folder, 'details.json')
        if not os.path.isfile(json_file_path):
            with open(json_file_path, 'w') as json_file:
                json.dump(new_data, json_file)
        else:
            with open(json_file_path, 'r+') as json_file:
                data = json.load(json_file)
                data.update(new_data)
                json_file.seek(0)
                json.dump(data, json_file)
                json_file.truncate()

    def set_video_data(self, vid_path,vid_folder,vid_extension):
        self.vid_path_original = vid_path
        self.vid_folder = vid_folder
        self.vid_extension = vid_extension
    
    def load_project_data(self,vid_folder):
        json_file_path = os.path.join(vid_folder, 'details.json')
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            self.vid_path_original = data['vid_path_original']
            self.vid_folder = data['vid_folder']
            self.vid_extension = data['vid_extension']
            self.vid_language = data['vid_language']
            self.dest_languages = data['dest_languages']
            self.are_captions_generated = data['are_captions_generated']
            self.captions_type = data['captions_type']

    def save_project_data(self):
        new_data = {
            'vid_path_original': self.vid_path_original,
            'vid_folder': self.vid_folder,
            'vid_extension': self.vid_extension,
            'vid_language': self.vid_language if hasattr(self, 'vid_language') else None,
            'dest_languages': self.dest_languages if hasattr(self, 'dest_languages') else None,
            'are_captions_generated': self.are_captions_generated if hasattr(self, 'are_captions_generated') else False,
            'captions_type': self.captions_type if hasattr(self, 'captions_type') else 'srt'
        }
        self.update_json_file(new_data)

    def generate_captions(self,source_lang: str, dest_langs: list, captions_type="srt"):
        # Your function logic here
        print('Source language:', source_lang)
        print('Destination languages:', dest_langs)
        self.vid_language = source_lang
        self.dest_languages = dest_langs
        self.captions_type = captions_type
        self.video_captioner.generate_captions(media_path=self.vid_path_original,vid_folder=self.vid_folder,
                                                source_lang=source_lang, dest_langs=dest_langs,captions_type=captions_type)
        self.are_captions_generated = True
        return None

    def get_captions(self,language: str):
        """
        Get captions for a specific language
        """
        try:
            captions = parse_captions(f"{self.vid_folder}/{language}.{self.captions_type}")
            return captions
        except FileNotFoundError:
            return []
    
    def save_captions(self,captions,language):
        """
        Save captions to a file
        """
        try:
            with open(f"{self.vid_folder}/{language}.{self.captions_type}", "w") as file:
                for i, caption in enumerate(captions):
                    file.write(f"{i+1}\n")
                    file.write(f"{caption['start']} --> {caption['end']}\n")
                    file.write(f"{caption['text']}\n\n")
        except Exception as e:
            return str(e)

    def add_captions(self,dest_langs):
        """
        If the generaeted captions are fine, add caption to video
        """
        self.dest_languages = dest_langs
        print("Adding captions to video",self.captions_type)
        if self.are_captions_generated:
            self.video_captioner.add_captions(vid_folder=self.vid_folder,vid_extension=self.vid_extension,
                                            dest_langs=dest_langs, captions_type=self.captions_type)
            return True
    
