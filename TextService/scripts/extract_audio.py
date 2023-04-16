from moviepy.editor import *

# Load video file
def extract_audio(filename):
    video = VideoFileClip(filename)
    # Extract audio from video
    audio = video.audio
    # Save audio file
    new_file_name = f"{filename[:-4].replace(' (online-video-cutter.com)','')}.mp3"
    audio.write_audiofile(new_file_name)
    return new_file_name