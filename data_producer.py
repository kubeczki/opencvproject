import cv2
import time
from logger import log, log_process_duration


def produce_data_std(queue, time_control_queue, filename):
    if filename == "no_filename":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(filename)

    while True:
        process_start = time.time()
        # Read the frame
        valid, img = cap.read()
        if not valid:
            print("ERROR: Image Error on VideoCapture\n")
            log(time.asctime(), "produce_data_std;", "No image input")
            break
        time_control_queue.put(time.time())
        queue.put(img)
        log(time.asctime(), "produce_data_std;", "Raw image has been captured and stored")
        time.sleep(0.1)

        # Stop if escape key is pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        process_duration = time.time() - process_start
        log_process_duration("produce_data_std", process_duration)

    # Release the VideoCapture object
    cap.release()
    # call this when we stop using the camera


def produce_data_alt(raw_image_pipe_in, time_control_pipe_in, filename):
    if filename == "no_filename":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(filename)

    while True:
        process_start = time.time()
        # Read the frame
        valid, img = cap.read()
        if not valid:
            print("ERROR: Image Error on VideoCapture\n")
            log(time.asctime(), "produce_data_alt;", "No image input")
            break
        time_control_pipe_in.send(time.time())
        raw_image_pipe_in.send(img)
        log(time.asctime(), "produce_data_alt;", "Raw image has been captured and stored")
        time.sleep(0.010)

        # Stop if escape key is pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        process_duration = time.time() - process_start
        log_process_duration("produce_data_alt", process_duration)

    raw_image_pipe_in.close()
    time_control_pipe_in.close()
    # Release the VideoCapture object
    cap.release()
    # call this when we stop using the camera


def produce_data_samp(raw_input_queue, detection_queue, time_control_queue, filename):
    if filename == "no_filename":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(filename)

    while True:
        process_start = time.time()
        # Read the frame
        valid, img = cap.read()
        if not valid:
            print("ERROR: Image Error on VideoCapture\n")
            log(time.asctime(), "produce_data_samp;", "No image input")
            break
        time_control_queue.put(time.time())
        raw_input_queue.put(img)
        detection_queue.put(img)
        log(time.asctime(), "produce_data_samp;", "Raw image has been captured and stored")
        time.sleep(0.01)

        # Stop if escape key is pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        process_duration = time.time() - process_start
        log_process_duration("produce_data_samp", process_duration)

    # Release the VideoCapture object
    cap.release()
    # call this when we stop using the camera