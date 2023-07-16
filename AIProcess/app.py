from genericpath import isdir
from flask import Flask, request
from flask_cors import CORS
import requests
import threading
import logging as log
import random
import json
import os

from scripts.extract_audio import extract_audio
from scripts.env_vars import *

env_vars = None
workers = None
free_workers = None

app = Flask(__name__)
CORS(app)
app.config['STATIC_FOLDER'] = 'static'
upload_folder = '../files'

log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')

def find_workers_to_process():
    global env_vars, workers, free_workers

    discovery_host = env_vars[DISCOVERY_SERVICE_ADDRESS]
    discovery_port = env_vars[DISCOVERY_SERVICE_PORT]
    response = requests.get(f'http://{discovery_host}:{discovery_port}/get_workers')
    response = json.loads(response.text)
    workers = response['workers']
    free_workers = [key for key in workers.keys()]
    log.info(f"Found {len(response['workers'])} workers, {free_workers}")
    return

@app.route("/request", methods=['POST'])
def apply_changes():
    global workers, free_workers

    form_data = request.form
    log.info("Processing request with following options: {}".format(form_data))
    file = request.files['video']
    if not os.path.isdir(upload_folder):
        os.mkdir(upload_folder)
    save_file_path = os.path.join(upload_folder, file.filename)
    file.save(save_file_path)
    form_data = dict(form_data)
    form_data['filename_video'] = save_file_path

    audio_file_name = extract_audio(save_file_path)
    form_data['filename_audio'] = audio_file_name

    # Finding all Free workers
    find_workers_to_process()
    worker_name = random.choice(free_workers) 
    free_workers.remove(worker_name)
    worker = workers[worker_name]

    log.info(f"Sending request to {worker_name}: {worker}")
    response = requests.post(f'{worker}/process', params=form_data)
    response = json.loads(response.text)
    log.info("Response from worker: {}".format(response))
    free_workers.append(worker_name)
    
    return {"status": "success", 'result': response['result'], 'video_url': response['video_url']}

if __name__ == '__main__':
    env_vars = EnvironmentVariables()
    app.run(host=env_vars[AI_PROCESS_SERVICE_ADDRESS], port=env_vars[AI_PROCESS_SERVICE_PORT], debug=True, use_reloader=False)