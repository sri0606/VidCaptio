from video import Video

if __name__ == "__main__":
    import sys

    media_path = sys.argv[1]
    caption_file_loc = sys.argv[2] if len(sys.argv) > 2 else "captions"
    captions_type = sys.argv[3] if len(sys.argv) > 3 else "srt"

    video = Video(media_path)
    video.add_captions(caption_file_loc, captions_type)