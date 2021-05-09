import multiprocessing as mp
from data_producer import produce_data, produce_data_alt
from image_modifier import display, display_alt
from face_detector import detect_faces, detect_faces_alt
import cv2
import time
import sys


def system_std():
    raw_input_queue = mp.Queue()
    processed_queue = mp.Queue()
    faces_queue = mp.Queue()

    producer = mp.Process(target=produce_data, args=(raw_input_queue,))
    producer.start()

    detector = mp.Process(target=detect_faces, args=(raw_input_queue, processed_queue, faces_queue, ))
    detector.start()

    displayer = mp.Process(target=display, args=(raw_input_queue, faces_queue,))
    displayer.start()

    producer.join()
    detector.join()
    displayer.join()

    # k = cv2.waitKey(30) & 0xff
    # if k == 27:
    #    time.sleep(0.1)
    #    sys.exit()
    return 0
