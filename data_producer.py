import cv2
import time


def produce_data(queue):
    # To capture video from webcam.
    cap = cv2.VideoCapture(0)

    while True:
        # Read the frame
        _, img = cap.read()

        queue.put(img)

        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
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
        _, img = cap.read()

        display_connection.send(img)
        time.sleep(0.010)

        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    raw_image_pipe_in.close()
    # Release the VideoCapture object
    cap.release()
    # call this when we stop using the camera
