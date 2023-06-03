import os

OPEN_API_KEY = 'YOUR API KEY'

MODEL_WHISPER_SIZE = 'small'
DEVICE = 'cuda'
IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
os.environ["IMAGEMAGICK_BINARY"] = IMAGEMAGICK_BINARY