from pydantic import BaseModel

class ProcessingResult(BaseModel):
    detected_language: str = None
    text: str = None
    final_video_path: str = None
    summarized_text: str = None
    face_blurred: bool = None
    license_plate_blurred: bool = None
    trimmed: bool = None