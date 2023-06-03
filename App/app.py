from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS

import requests
import threading
import logging as log

from config import *
from scripts.models import *
from scripts.env_vars import *

app = Flask(__name__)
CORS(app)
app.config['STATIC_FOLDER'] = 'static'

log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')


@app.route("/", methods=['GET'])
def home():
    log.info(str(request))
    return render_template("index.html")

@app.route('/video_editing')
def video_editing():
    return render_template('video-editing.html')

@app.route("/apply", methods=['POST'])
def apply():
    response_data = {'status': 'ok'}
    return response_data


if __name__ == "__main__":
    env_vars = EnvironmentVariables()
    app.run(host=env_vars[APP_SERVICE_ADDRESS], port=env_vars[APP_SERVICE_PORT], debug=True)