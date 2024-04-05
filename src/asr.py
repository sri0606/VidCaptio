import stable_whisper
import re

def convert_time(time):
    # Convert the time to hours, minutes, and seconds
    hours, remainder = divmod(time, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format the time as a string
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int((seconds - int(seconds)) * 1000):03}"

class Transcriber():
    def __init__(self,model_path):
        self.recognizer  = stable_whisper.load_model(model_path)

    def get_transcript(self,media_path, minimum_sentence_length=5, max_sentence_length=23):
        """
        Generate transcript using stable_whisper's version of OpenAI's Whisper

        Parameter:
         -  minimum_sentence_length : minimu number of words in sentence/transcript of each clip
        """
        transcript = {}
        result = self.recognizer.transcribe(media_path)

        transcript["text"] = result.text
        #get word level timsestamps
        word_lev_ts = result.all_words_or_segments()

        transcript["segments"] = self.__generate_sentence_level_transcript(word_timestamps=word_lev_ts,minimum_sentence_length=minimum_sentence_length,max_sentence_length=max_sentence_length)

        return transcript


    def __generate_sentence_level_transcript(self,word_timestamps, minimum_sentence_length=5,max_sentence_length=20, skip_punctuations=["Dr.", "Mr.", "Mrs.", "Ms.",'Jr.',"Sr."]):
        """
        Generates sentence level timestamps from a list of word level timestamps.

        Args:
            word_timestamps (list): A list of word level timestamps. Each timestamp is expected to be an object with 'start', 'end', and 'word' attributes.
            minimum_sentence_length (int, optional): The minimum number of words a sentence should have to be included in the output. Defaults to 10.
            skip_punctuations (list, optional): A list of abbreviations that should not be treated as the end of a sentence. Defaults to ["Dr.", "Mr.", "Mrs.", "Ms.",'Jr.',"Sr."].

        Returns:
            list: A list of sentence level timestamps. Each timestamp is a dictionary with 'start', 'end', and 'text' keys. 'start' and 'end' are the start and end times of the sentence, and 'text' is the sentence text.
        """
        sentences = []
        current_sentence_start = word_timestamps[0].start
        current_sentence_words = []
        
        clip_id = 0
        for i,word_timing in enumerate(word_timestamps):
            current_sentence_words.append(word_timing.word)
            if  len(current_sentence_words)>=max_sentence_length or (word_timing.word.endswith(('.', '!', '?')) and word_timing.word not in skip_punctuations and not re.match("^\d+?\.\d+?$", word_timing.word)):
                if len(current_sentence_words) >= minimum_sentence_length:
                    sentences.append({
                        'clip_id' : clip_id,
                        'start': convert_time(current_sentence_start),
                        'end': convert_time(word_timing.end),
                        'text': ' '.join(current_sentence_words)
                    })
                else:
                    continue
                if word_timing != word_timestamps[-1]:
                    current_sentence_start = word_timestamps[i+1].start
                current_sentence_words = []
                clip_id+=1
        
        if current_sentence_words and len(current_sentence_words) >= minimum_sentence_length:
            sentences.append({
                'clip_id':clip_id,
                'start': current_sentence_start,
                'end': word_timestamps[-1].end,
                'sentence': ' '.join(current_sentence_words)
            })
        
        return sentences
    
    def generate_caption_file(self,media_path,filepath,type="srt"):
        """
        Generate caption file from the transcript

        Args:
            type (str, optional): The type of caption file to generate. Defaults to "srt".
            filename (str, optional): The name of the caption file to generate. Defaults to "captions".
        """
        if type == "srt":
            self.__generate_srt_file(media_path,filepath)

        elif type == "vtt":
            self.__generate_vtt_file(media_path,filepath)
        else:
            raise ValueError(f"Unsupported caption file type: {type}")
        
    def __generate_srt_file(self,media_path,filepath):
        """
        Generate SRT file from the transcript

        Args:
            filename (str): The name of the SRT file to generate.
        """
        transcript = self.get_transcript(media_path)
        with open(f"{filepath}.srt", "w") as f:
            for i,segment in enumerate(transcript["segments"]):
                f.write(f"{i+1}\n")
                f.write(f"{segment['start']} --> {segment['end']}\n")
                f.write(f"{segment['text']}\n\n")

    def __generate_vtt_file(self,media_path,filepath):
        """
        Generate VTT file from the transcript

        Args:
            filename (str): The name of the VTT file to generate.
        """
        transcript = self.get_transcript(media_path)
        with open(f"{filepath}.vtt", "w") as f:
            f.write("WEBVTT\n\n")
            for i,segment in enumerate(transcript["segments"]):
                f.write(f"{i+1}\n")
                f.write(f"{segment['start']} --> {segment['end']}\n")
                f.write(f"{segment['text']}\n\n")