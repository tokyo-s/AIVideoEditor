from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS
import requests
import threading
import logging as log
import os
from scripts.summarizer import summarize
from scripts.transcriber import transcribe
from scripts.extract_audio import extract_audio
from config import *
from scripts.models import *

app = Flask(__name__)
CORS(app)
app.config['STATIC_FOLDER'] = 'static'
upload_folder = '../files'

log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')

@app.route("/process", methods=['POST'])
def apply_changes():
    file = request.files['video']
    save_file_path = os.path.join(upload_folder, file.filename)
    file.save(save_file_path)
    new_file_name = extract_audio(save_file_path)
    form_data = request.form
    detected_language, video_text = transcribe(new_file_name)
    result = summarize(video_text)
    log.info("Processing request with following options: {}".format(form_data))
    return {"status": "success", "result":result}

if __name__ == '__main__':
    app.run(host="localhost", port=8001)