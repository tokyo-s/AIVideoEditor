from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS

import requests
import threading
import logging as log

from config import *
from scripts.models import *

app = Flask(__name__)
CORS(app)
app.config['STATIC_FOLDER'] = 'static'

log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')


@app.route("/", methods=['GET'])
def home():
    print(request)
    log.info(str(request))
    return render_template("index.html")

@app.route('/video_editing')
def video_editing():
    return render_template('video-editing.html')

@app.route("/apply", methods=['POST'])
def apply():
    print(request)
    response_data = {'status': 'ok'}
    return response_data


if __name__ == "__main__":
    app.run(host="localhost", port=8000)