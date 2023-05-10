from flask import Flask, jsonify, request
from flask_cors import CORS
import logging as log

from scripts.env_vars import *

app = Flask(__name__)

# Example list of services with their URLs
services = {}
env_vars = None

CORS(app)
log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')

@app.route('/discover', methods=['GET'])
def discover_service():
    service_name = request.args.get('name')

    if service_name in services:
        return jsonify({"url": services[service_name]})
    else:
        return jsonify({"error": "Service not found"}), 404
    
@app.route('/get_workers', methods=['GET'])
def discover_worker():
    return jsonify({"workers": services})
    
@app.route('/register', methods=['POST'])
def register_service():
    global services

    service_name = request.args.get('name')
    service_address = request.args.get('address')
    service_port = request.args.get('port')

    if service_name in services:
        return jsonify({"message": "Service already registered"}), 400
    else:
        services[service_name] = f"http://{service_address}:{service_port}"
        return jsonify({"message": "Service registered successfully"}), 200


if __name__ == '__main__':
    env_vars = EnvironmentVariables()
    app.run(debug=True, host=env_vars[DISCOVERY_SERVICE_ADDRESS], port=env_vars[DISCOVERY_SERVICE_PORT])