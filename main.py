import multiprocessing as mp
import numpy as np
import cv2 as cv
import os
from data_producer import produce_data
from image_modifier import display
from face_detector import detect_faces


if __name__ == '__main__':

    raw_input_queue = mp.Queue(1)
    processed_queue = mp.Queue()
    faces_queue = mp.Queue()

    producer = mp.Process(target=produce_data, args=(raw_input_queue,))
    producer.start()

    detector = mp.Process(target=detect_faces, args=(raw_input_queue, processed_queue, faces_queue, ))
    detector.start()

    displayer = mp.Process(target=display, args=(processed_queue, faces_queue, ))
    displayer.start()

    producer.join()
    detector.join()
    displayer.join()
