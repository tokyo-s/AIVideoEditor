from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS
import requests
import json
import logging as log
from config import *
from scripts.models import *
from scripts.worker import Worker
from scripts.env_vars import *

env_vars = None

app = Flask(__name__)
CORS(app)
app.config['STATIC_FOLDER'] = 'static'
upload_folder = '../files'

log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')

def register_worker():
    global env_vars
    env_vars = EnvironmentVariables()
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

@app.route("/process", methods=['POST'])
def apply_changes():
    global env_vars

    args = request.args
    log.info("Processing request with following options: {}".format(args))
    worker = Worker(env_vars[WORKER_NAME], args)
    result = worker.work()
    return {"status": "success", "result":result}

if __name__ == '__main__':
    register_worker()
    app.run(host=env_vars[WORKER_ADDRESS], port=env_vars[WORKER_PORT], debug=True, use_reloader=False)