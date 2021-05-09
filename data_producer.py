import cv2
import time


def produce_data(queue):
    # To capture video from webcam.
    cap = cv2.VideoCapture(0)

    while True:
        # Read the frame
        valid, img = cap.read()
        if not valid:
            print("ERROR: Image Error on VideoCapture\n")
            break
        queue.put(img)
        time.sleep(0.1)

        # Stop if escape key is pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    # Release the VideoCapture object
    cap.release()
    # call this when we stop using the camera


def produce_data_alt(raw_image_pipe_in):
    # To capture video from webcam.
    cap = cv2.VideoCapture(0)

    while True:
        # Read the frame
        valid, img = cap.read()
        if not valid:
            print("ERROR: Image Error on VideoCapture\n")
            break
        raw_image_pipe_in.send(img)
        time.sleep(0.010)

        # Stop if escape key is pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    raw_image_pipe_in.close()
    # Release the VideoCapture object
    cap.release()
    # call this when we stop using the camera


def produce_data_samp(raw_image_pipe_in, raw_image_det_pipe_in):
    # To capture video from webcam.
    cap = cv2.VideoCapture(0)
    while True:
        # Read the frame
        valid, img = cap.read()
        if not valid:
            print("ERROR: Image Error on VideoCapture\n")
            break
        raw_image_pipe_in.send(img)
        raw_image_det_pipe_in.send(img)
        time.sleep(0.010)

        # Stop if escape key is pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    raw_image_pipe_in.close()
    raw_image_det_pipe_in.close()
    # Release the VideoCapture object
    cap.release()
    # call this when we stop using the camera
