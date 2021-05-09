import multiprocessing as mp
from data_producer import produce_data_alt
from image_modifier import modify_alt
from face_detector import detect_faces_alt
import cv2
import time
import sys


def system_alt():
    # producer - detector pipe
    raw_image_pipe_in, raw_image_pipe_out = mp.Pipe()
    # detector - displayer image pipe
    processed_image_pipe_in, processed_image_pipe_out = mp.Pipe()
    # detector - displayer faces locations pipe
    faces_in, faces_out = mp.Pipe()

    producer = mp.Process(target=produce_data_alt, args=(raw_image_pipe_in, ))
    producer.start()

    detector = mp.Process(target=detect_faces_alt, args=(raw_image_pipe_out, processed_image_pipe_in, faces_in,))
    detector.start()

    displayer = mp.Process(target=modify_alt, args=(processed_image_pipe_out, faces_out, ))
    displayer.start()

    producer.join()
    detector.join()
    displayer.join()

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        sys.exit()
