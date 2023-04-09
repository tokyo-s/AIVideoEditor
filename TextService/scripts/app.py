from fastapi import FastAPI, Request, File, UploadFile, Form
import requests
import threading
import logging as log
import uvicorn

from config import *
from models import *

app = FastAPI()
log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')

@app.post("/process")
async def apply_changes(options: VideoOptions):

    log.info("Processing request with following options: {}".format(options.dict()))
    return {"status": "success"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
