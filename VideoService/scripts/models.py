from pydantic import BaseModel

class VideoOptions(BaseModel):
    trim_start: bool
    trim_end: bool
    add_title: bool
    add_subtitles: bool
    black_and_white: bool
    sepia: bool