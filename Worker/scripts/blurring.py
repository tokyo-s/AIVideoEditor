import numpy as np
import logging as log
from moviepy.editor import AudioFileClip, VideoFileClip
import argparse
import time
import cv2
import os


CONFIDENCE_THRESHOLD = 0.5
net = None
plate_cascade = None

log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')

def load_models():
    global net, plate_cascade
     # load our serialized face detector model from disk
    log.info("Loading face detector model...")
    prototxtPath ="models/deploy.prototxt"
    weightsPath = "models/res10_300x300_ssd_iter_140000.caffemodel"
    net = cv2.dnn.readNet(prototxtPath, weightsPath)
    plate_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")

def blur_simple(image, factor=3.0):
	# automatically determine the size of the blurring kernel based
	# on the spatial dimensions of the input image
	(h, w) = image.shape[:2]
	kW = int(w / factor)
	kH = int(h / factor)
	# ensure the width of the kernel is odd
	if kW % 2 == 0:
		kW -= 1
	# ensure the height of the kernel is odd
	if kH % 2 == 0:
		kH -= 1
	# apply a Gaussian blur to the input image using our computed
	# kernel size
	return cv2.GaussianBlur(image, (kW, kH), 0)


def blur(video_path, audio_path, faces=False, plates=False):
    global net, plate_cascade

    if not net:
        load_models()
    log.info("Starting video stream...")

    cap = cv2.VideoCapture(video_path)
    audio = AudioFileClip(audio_path)

    # Get the video's width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frames_per_second = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For .mp4 format

    if '_result' not in video_path:
        output_video = video_path.replace('.mp4', '_result.mp4').replace('files','App/static')
    else:
        output_video = video_path.replace('result', 'blurred')

    out = cv2.VideoWriter(output_video, fourcc, frames_per_second, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        # grab the dimensions of the frame and then construct a blob
        # from it
        (h, w) = frame.shape[:2]

        if faces:
            blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                (104.0, 177.0, 123.0))
            # pass the blob through the network and obtain the face detections
            net.setInput(blob)
            detections = net.forward()
            # loop over the detections
            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > CONFIDENCE_THRESHOLD:
                    # compute the (x, y)-coordinates of the bounding box for
                    # the object
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # extract the face ROI
                    face = frame[startY:endY, startX:endX]
                    face = blur_simple(face, factor=3.0)

                    # store the blurred face in the output image
                    frame[startY:endY, startX:endX] = face

        if plates:
            plate=plate_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=3)
            for x, y, w, h in plate:
                startX, startY, endX, endY = x, y, x+w, y+h
                plate = frame[startY:endY, startX:endX]
                plate = blur_simple(plate, factor=3.0)
                frame[startY:endY, startX:endX] = plate
                # blur_image = cv2.GaussianBlur(frame,(23, 23), 30)
                # blur_image[y:y+plate.shape[0], x:x+plate.shape[1]] = plate
        out.write(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    video_clip = VideoFileClip(output_video)
    final_clip = video_clip.set_audio(audio)

    if '_result' not in output_video:
        output_video = output_video.replace('blurred', 'result')
    else:
        output_video = output_video.replace('result', 'blurred')

    final_clip.write_videofile(output_video, codec='libx264', audio_codec="libmp3lame")

    return output_video
