from scripts.summarizer import summarize
from scripts.transcriber import transcribe

class Worker:
    def __init__(self, name, arguments):
        for key, value in arguments.items():
            setattr(self, key, value)

        self.name = name
        self.text = None
        self.detected_language = None
        self.summarized_text = None

    def work(self):
        print(f'{self.name} is working...')

        if self.add_subtitles:
            self.detected_language, self.text = transcribe(self.filename_audio)

        # if self.summarize:
        #     if self.text is None:
        #         self.detected_language, self.text = transcribe(self.audio_filename)
        #     self.summarized_text = summarize(self.text)
        return
