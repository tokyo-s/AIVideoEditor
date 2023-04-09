from fastapi import FastAPI
import requests
import threading
import logging
import uvicorn

app = FastAPI()
logger = logging.getLogger(__name__)


@app.post("/post-data")
async def handle_post_data(request_data: dict):

    print(request_data)

    response_data = {'status': 'ok'}
    return response_data

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
