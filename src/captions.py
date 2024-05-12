import translators
import os
import webvtt
import pysrt

def translate(text,srclan,destlan):
    """
    helper function to translate text from one language to another

    Args:
        text (str): The text to translate
        srclan (str): The source language
        destlan (str): The destination language
    """
    return translators.translate_text(query_text=text,from_language=srclan,to_language=destlan)

def generate_caption_file(transcript,srclan,destlan,type,captions_folder_path):
    """
    Generate caption file from the transcript

    Args:
        type (str, optional): The type of caption file to generate. Defaults to "srt".
        filename (str, optional): The name of the caption file to generate. Defaults to "captions".
    """
    if type != "srt" and type != "vtt":
        raise ValueError(f"Unsupported caption file type: {type}")
    
    with open(f"{captions_folder_path}/{destlan}.{type}", "w",encoding='utf-8') as f:
        for i,segment in enumerate(transcript["segments"]):
            if srclan!=destlan:
                translated_text = translate(segment['text'], srclan, destlan)
            else:
                translated_text = segment['text']
            f.write(f"{i+1}\n")
            f.write(f"{segment['start']} --> {segment['end']}\n")
            f.write(f"{translated_text}\n\n")
    

def generate_captions(transcript,srclan, languages,type,captions_folder):
    """
    Generates caption files for the transcript in the specified languages

    Args:
        transcript (dict): A dictionary containing the transcript of the video. The dictionary should have 'text' and 'segments' keys. 'text' is the full transcript of the video, and 'segments' is a list of dictionaries containing the start and end times and the text of each segment of the transcript.
        languages (list): A list of languages to generate captions for.
        type (str): The type of caption file to generate.
        captions_folder (str): The folder to save the caption files to.
    """
    for language in languages:
        generate_caption_file(transcript,srclan,destlan=language,type=type,captions_folder_path=captions_folder)
        #get the transcript in the language

def parse_captions(file_path):
    captions = []
    if file_path.endswith('.vtt'):
        for caption in webvtt.read(file_path):
            captions.append({
                'start': str(caption.start),
                'end': str(caption.end),
                'text': caption.text.strip()
            })
    elif file_path.endswith('.srt'):
        for caption in pysrt.open(file_path):
            captions.append({
                'start': str(caption.start),
                'end': str(caption.end),
                'text': caption.text.strip()
            })
    else:
        raise ValueError('Unsupported caption file type')
    return captions