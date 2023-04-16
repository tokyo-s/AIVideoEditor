from moviepy.editor import *
import logging as log
log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')

# Load video file
def extract_audio(filename):
    log.info("Extracting audio from video file: {}".format(filename))
    video = VideoFileClip(filename)
    # Extract audio from video
    audio = video.audio
    # Save audio file
    new_file_name = f"{filename[:-4].replace(' (online-video-cutter.com)','')}.mp3"
    audio.write_audiofile(new_file_name)
    return new_file_name