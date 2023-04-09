from fastapi import FastAPI, Request, File, UploadFile, Form
import requests
import threading
import logging as log
import uvicorn

from summarizer import summarize
from transcriber import transcribe
from extract_audio import extract_audio
from config import *
from models import *

app = FastAPI()
log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')

@app.post("/process")
async def apply_changes(options: VideoOptions):
    extract_audio(options.filename)
    video_text = transcribe(options.filename[:-4] + ".mp3")
    result = summarize(video_text)
    log.info("Processing request with following options: {}".format(options.dict()))
    return {"status": "success", "result":result}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
