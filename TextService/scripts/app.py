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
async def apply_changes(video: UploadFile = File(...)):
    new_file_name = extract_audio(options.filename)
    detected_language, video_text = transcribe(new_file_name)
    result = summarize(video_text)
    log.info("Processing request with following options: {}".format(options.dict()))
    return {"status": "success", "result":result}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
