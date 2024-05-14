from src.video import Video

if __name__ == "__main__":
    import sys

    media_path = sys.argv[1]
    src_language = sys.argv[2] if len(sys.argv) > 2 else "en"
    dest_languages = sys.argv[3].split(',') if len(sys.argv) > 3 else ["es"]
    caption_file_loc = sys.argv[4] if len(sys.argv) > 4 else "captions"
    captions_type = sys.argv[5] if len(sys.argv) > 5 else "srt"

    video = Video(media_path,language=src_language)
    video.add_captions(dest_langs=dest_languages,caption_file_loc=caption_file_loc, captions_type=captions_type)