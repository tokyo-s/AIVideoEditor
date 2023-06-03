from scripts.summarizer import summarize
from scripts.transcriber_timestampted import transcribe_timestamped
from scripts.subtitles import add_subtitles_on_video
from scripts.translator import translate, translate_subtitles
from scripts.models import ProcessingResult
from scripts.blurring import blur
from scripts.trimmer import trim_video

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

        if self.subtitles or self.summarize:
            self.detected_language, self.transcribtion = transcribe_timestamped(self.filename_audio)
            self.original_text = self.transcribtion['text']
            self.text = self.transcribtion['text']
            result.detected_language = self.detected_language
            result.text = self.text

        if self.translate_subtitles:
            self.text = translate(self.text, 'ro')
            self.transcribtion['segments'] = translate_subtitles(self.transcribtion['segments'], 'ro') 
            result.text = self.text
        
        if self.add_subtitles:
            self.current_video_path = add_subtitles_on_video(self.transcribtion, self.current_video_path)

        if self.summarize:
            self.summarized_text = summarize(self.text)
            result.summarized_text = self.summarized_text

        if self.blur_faces or self.blur_license_plates:
            blurred = blur(self.current_video_path, self.blur_faces, self.blur_license_plates)
            result.face_blurred = blurred
            result.license_plate_blurred = blurred

        if self.trim:
            result.trimmed = trim_video(self.current_video_path, self.trim_start, self.trim_end)

        self.busy = False
        return result


