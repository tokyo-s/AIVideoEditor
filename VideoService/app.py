from fastapi import FastAPI
import requests
import threading
import logging
import uvicorn

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/")
async def home():
    url = 'http://text-container:8001/post-data'
    data = {'key1': 'value1', 'key2': 'value2'}
    response = requests.post(url, json=data)
    return response


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8002)


