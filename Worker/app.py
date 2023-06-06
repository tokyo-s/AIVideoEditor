from flask import Flask, request, url_for, jsonify
from flask_cors import CORS
import requests
import json
import logging as log
from config import *
from scripts.models import *
from scripts.worker import Worker
from scripts.env_vars import *
import argparse

env_vars = None
worker = None

app = Flask(__name__)
CORS(app)
app.config['STATIC_FOLDER'] = 'static'
upload_folder = '../files'

log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')

def register_worker():
    global env_vars
    discovery_host = env_vars[DISCOVERY_SERVICE_ADDRESS]
    discovery_port = env_vars[DISCOVERY_SERVICE_PORT]
    worker_name = env_vars[WORKER_NAME]
    worker_address = env_vars[WORKER_ADDRESS]
    worker_port = env_vars[WORKER_PORT]

    log.info(f'Registering worker at {worker_address}:{worker_port}')
    response = requests.post(f"http://{discovery_host}:{discovery_port}/register", params={"name": worker_name, "address": worker_address, 'port': worker_port})
    response = json.loads(response.text)
    log.info(f'Discovery Service: {response["message"]}')
    return

@app.route("/health-check", methods=['GET'])
def health_check():
    global worker, env_vars

    log.info(f"Checking health of {env_vars[WORKER_NAME]}")
    if worker is None or worker.busy==False:
        return jsonify({"status": "success", "status": "Free"}, 200)
    elif worker.busy:
        return jsonify({"status": "success", "status": "Busy"}, 200)

@app.route("/process", methods=['POST'])
def apply_changes():
    global env_vars, worker

    args = request.args
    log.info("Processing request with following options: {}".format(args))
    worker = Worker(env_vars[WORKER_NAME], args)
    result = worker.work()
    log.info("Processing request finished")
    final_video_path = result.final_video_path.replace('App/', '')
    return {"status": "success", "result":result.__dict__, 'video_url': final_video_path}

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str, required=False)
    parser.add_argument('--name', type=str, required=False)

    args = parser.parse_args()
    os.environ["WORKER_NAME"] = args.name
    os.environ["WORKER_PORT"] = args.port
    
    env_vars = EnvironmentVariables()
    print(env_vars[WORKER_ADDRESS], env_vars[WORKER_PORT])
    register_worker()
    app.run(host=env_vars[WORKER_ADDRESS], port=env_vars[WORKER_PORT], debug=True, use_reloader=False) 