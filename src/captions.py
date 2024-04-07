import translators
import os

class Captioner():
    def __init__(self,media_path):
        self.media_path = media_path
        return
    
    def __translate__(self, text,srclan,destlan):
        """
        helper function to translate text from one language to another

        Args:
            text (str): The text to translate
            srclan (str): The source language
            destlan (str): The destination language
        """
        return translators.translate_text(query_text=text,from_language=srclan,to_language=destlan)
    

    def generate_captions(self,transcript,srclan, languages,type,captions_folder):
        """
        
        """
        #create a captions folder if it doesnt exist
        captions_folder_path = os.path.join(os.getcwd(), captions_folder)
        os.makedirs(captions_folder_path, exist_ok=True)

        for language in languages:

            self.generate_caption_file(transcript,srclan,destlan=language,type=type,captions_folder_path=captions_folder_path)
            #get the transcript in the language

    def generate_caption_file(self,transcript,srclan,destlan,type,captions_folder_path):
        """
        Generate caption file from the transcript

        Args:
            type (str, optional): The type of caption file to generate. Defaults to "srt".
            filename (str, optional): The name of the caption file to generate. Defaults to "captions".
        """
        if type == "srt":
            self.__generate_srt_file(transcript,srclan,destlan,captions_folder_path)

        elif type == "vtt":
            self.__generate_vtt_file(transcript,srclan,destlan,captions_folder_path)
        else:
            raise ValueError(f"Unsupported caption file type: {type}")
        
    def __generate_srt_file(self,transcript,srclan,destlan,captions_folder_path):
        """
        Generate SRT file from the transcript

        Args:
            filename (str): The name of the SRT file to generate.
        """
        
        with open(f"{captions_folder_path}/{destlan}.srt", "w",encoding='utf-8') as f:
            for i,segment in enumerate(transcript["segments"]):
                if srclan!=destlan:
                    translated_text = self.__translate__(segment['text'], srclan, destlan)
                else:
                    translated_text = segment['text']
                f.write(f"{i+1}\n")
                f.write(f"{segment['start']} --> {segment['end']}\n")
                f.write(f"{translated_text}\n\n")

    def __generate_vtt_file(self,transcript,srclan,destlan,captions_folder_path):
        """
        Generate VTT file from the transcript

        Args:
            filename (str): The name of the VTT file to generate.
        """
        with open(f"{captions_folder_path}/{destlan}.vtt", "w",encoding='utf-8') as f:
            for i,segment in enumerate(transcript["segments"]):               
                if srclan!=destlan:
                    translated_text = self.__translate__(segment['text'], srclan, destlan)
                else:
                    translated_text = segment['text']
                f.write(f"{i+1}\n")
                f.write(f"{segment['start']} --> {segment['end']}\n")
                f.write(f"{translated_text}\n\n")