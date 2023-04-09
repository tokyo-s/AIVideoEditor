from moviepy.editor import *

# Load video file
def extract_audio(filename):
    video = VideoFileClip(filename)
    # Extract audio from video
    audio = video.audio
    # Save audio file
    audio.write_audiofile(f"{filename}.mp3")