from src.video import Video

class VidCaptioAPI:
    def __init__(self):
        self.video_captioner = Video()

    def set_video_data(self, vid_path,vid_folder,vid_extension):
        self.vid_path_original = vid_path
        self.vid_folder = vid_folder
        self.vid_extension = vid_extension
    
    def generate_captions(self,source_lang: str, dest_langs: list):
        # Your function logic here
        print('Source language:', source_lang)
        print('Destination languages:', dest_langs)

        captions = [{"start":"0:00", "end":"0:05", "text":"Hello, how are you?"}, 
                    {"start":"0:05", "end":"0:10", "text":"I am fine, thank you."}, 
                    {"start":"0:10", "end":"0:15", "text":"How about you?"}, 
                    {"start":"0:15", "end":"0:20", "text":"I am good too."},
                    {"start":"0:00", "end":"0:05", "text":"Hello, how are you?"}, 
                    {"start":"0:05", "end":"0:10", "text":"I am fine, thank you."}, 
                    {"start":"0:10", "end":"0:15", "text":"How about you?"}, 
                    {"start":"0:15", "end":"0:20", "text":"I am good too."},
                    {"start":"0:00", "end":"0:05", "text":"Hello, how are you?"}, 
                    {"start":"0:05", "end":"0:10", "text":"I am fine, thank you."}, 
                    {"start":"0:10", "end":"0:15", "text":"How about you?"}, 
                    {"start":"0:15", "end":"0:20", "text":"I am good too."}]
        
        self.video_captioner.generate_captions(media_path=self.vid_path_original,vid_folder=self.vid_folder,
                                                source_lang=source_lang, dest_langs=dest_langs)
        return captions

    def add_captions(self, dest_langs: list,captions_type="srt"):
        """
        If the generaeted captions are fine, add caption to video
        """
        self.video_captioner.add_captions(vid_folder=self.vid_folder,vid_extension=self.vid_extension,
                                        dest_langs=dest_langs, captions_type=captions_type)
        return True
    
