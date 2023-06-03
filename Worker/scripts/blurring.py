import numpy as np
import logging as log
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
    prototxtPath ="deploy.prototxt"
    weightsPath = "res10_300x300_ssd_iter_140000.caffemodel"
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


def blur(video_path, faces=False, plates=False):
    global net, plate_cascade

    if not net:
        load_models()
    log.info("Starting video stream...")



    cap = cv2.VideoCapture(video_path)

    # Get the video's width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For .mp4 format
    out = cv2.VideoWriter('output.mp4', fourcc, 30, (frame_width, frame_height))

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
        cv2.imshow("Output", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return True
