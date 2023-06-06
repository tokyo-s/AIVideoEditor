from scripts.summarizer import summarize
from scripts.transcriber_timestampted import transcribe_timestamped
from scripts.subtitles import add_subtitles_on_video
from scripts.translator import translate, translate_subtitles
from scripts.models import ProcessingResult
from scripts.blurring import blur
from scripts.trimmer import trim_video
import logging as log

log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')

class Worker:
    def __init__(self, name, arguments):
        for key, value in arguments.items():
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
            setattr(self, key, value)

        self.name = name
        self.current_video_path = self.filename_video
        self.busy = True
        self.transcribtion = None
        self.original_text = None
        self.text = None
        self.subtitles = []
        self.detected_language = None
        self.summarized_text = None

    def work(self):
        print(f'{self.name} is working...')
        result = ProcessingResult()

        if self.add_subtitles or self.summarize or self.translate_subtitles:
            log.info("Starting video transcribtion...")
            self.detected_language, self.transcribtion = transcribe_timestamped(self.filename_audio)
            self.original_text = self.transcribtion['text']
            self.text = self.transcribtion['text']
            result.detected_language = self.detected_language
            result.text = self.text
            log.info("Video transcribtion finished...")

        if self.translate_subtitles:
            log.info("Starting text translation...")
            self.text = translate(self.text, 'ro')
            self.transcribtion['segments'] = translate_subtitles(self.transcribtion['segments'], 'ro') 
            result.text = self.text
            log.info("Text translation finished...")
        
        if self.add_subtitles:
            log.info("Starting creating subtitles...")
            self.current_video_path = add_subtitles_on_video(self.transcribtion, self.current_video_path)
            log.info("Subtitles creation finished...")

        if self.summarize:
            log.info("Starting summarizing video...")
            self.summarized_text = summarize(self.text)
            result.summarized_text = self.summarized_text
            log.info("Summarizing video finished...")

        if self.blur_faces or self.blur_license_plates:
            log.info("Starting Bluring faces on video...")
            self.current_video_path = blur(self.current_video_path, self.filename_audio, self.blur_faces, self.blur_license_plates)
            result.face_blurred = True
            result.license_plate_blurred = True
            log.info("Bluring faces on video finished...")

        if self.trim_start or self.trim_end:
            log.info("Starting trimming video...")
            start_trim_seconds = 0 if not self.trim_start else 5
            end_trim_seconds = None if not self.trim_end else 5
            self.current_video_path = trim_video(self.current_video_path, start_trim_seconds, end_trim_seconds)
            result.trimmed = True
            log.info("Trimming video finished...")

        result.final_video_path = self.current_video_path
        self.busy = False
        return result


