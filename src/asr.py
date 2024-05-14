import stable_whisper
import re
import bisect

#skip abbraviations that be misread as punctuations
SKIP_ABBREVIATIONS=["dr." ,'jr.',"mr.", "mrs.", "ms.","sr."]

def convert_time(time):
    # Convert the time to hours, minutes, and seconds
    hours, remainder = divmod(time, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format the time as a string
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int((seconds - int(seconds)) * 1000):03}"

def is_skip_abbreviation(word):
    word = str(word).lower()
    index = bisect.bisect_left(SKIP_ABBREVIATIONS, word)
    return index != len(SKIP_ABBREVIATIONS) and SKIP_ABBREVIATIONS[index] == word

class Transcriber():
    def __init__(self,model_path):
        self.recognizer  = stable_whisper.load_model(model_path)

    def get_transcript(self,media_path, source_lang, min_char_length=35, max_char_length=45):
        """
        Generate transcript using stable_whisper's version of OpenAI's Whisper

        Parameter:
         -  minimum_sentence_length : minimu number of words in sentence/transcript of each clip
        """
        transcript = {}
        if source_lang:
            options = {"language": source_lang}
        else:
            options = {"language":None}
        result = self.recognizer.transcribe(media_path, **options)

        transcript["text"] = result.text
        #get word level timsestamps
        word_lev_ts = result.all_words_or_segments()

        transcript["segments"] = self.__generate_sentence_level_transcript(word_timestamps=word_lev_ts,min_char_length=min_char_length,max_char_length=max_char_length)

        return transcript


    def __generate_sentence_level_transcript(self,word_timestamps, min_char_length,max_char_length):
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
        current_char_len = 0
        clip_id = 0
        for i,word_timing in enumerate(word_timestamps):
            current_sentence_words.append(word_timing.word)
            current_char_len += len(word_timing.word)
            if  current_char_len>=max_char_length or (word_timing.word.endswith(('.', '!', '?')) and not is_skip_abbreviation(word_timing.word) and not re.match("^\d+?\.\d+?$", word_timing.word)):
                if current_char_len >= min_char_length:
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
                current_char_len = 0
                clip_id+=1
        
        if current_sentence_words and current_char_len >= min_char_length:
            sentences.append({
                'clip_id':clip_id,
                'start': current_sentence_start,
                'end': word_timestamps[-1].end,
                'sentence': ' '.join(current_sentence_words)
            })
        
        return sentences
    