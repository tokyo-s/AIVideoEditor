from fastapi import FastAPI, Request, File, UploadFile, Form
import requests
import threading
import logging as log
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from config import *
from models import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    print(request)
    log.info(str(request))
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )


@app.post("/apply-changes")
async def apply_changes(
    video: UploadFile = File(...),
    trim_start: bool = Form(False),
    trim_end: bool = Form(False),
    add_title: bool = Form(False),
    add_subtitles: bool = Form(False),
    black_and_white: bool = Form(False),
    sepia: bool = Form(False),
):
    options = VideoOptions(
        filename=f"files/{video.filename}",
        trim_start=trim_start,
        trim_end=trim_end,
        add_title=add_title,
        add_subtitles=add_subtitles,
        black_and_white=black_and_white,
        sepia=sepia,
    )
    # Save the video file
    with open(f"files/{video.filename}", "wb") as f:
        f.write(await video.read())

    log.info('Sending request to Video Service')
    requests.post(f'{VIDEO_SERVICE_ADDRESS}:{VIDEO_SERVICE_PORT}/process', json=options.dict())

    log.info('Sending request to Text Service')
    result = requests.post(f'{TEXT_SERVICE_ADDRESS}:{TEXT_SERVICE_PORT}/process', json=options.dict())
    log.info(result.dict())
    return {"status": "success"}


@app.post("/apply")
async def home(request: Request):
    print(request)
    response_data = {'status': 'ok'}
    return response_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
