import multiprocessing as mp
from data_producer import produce_data, produce_data_alt
from image_modifier import display, display_alt
from face_detector import detect_faces, detect_faces_alt
import cv2
import time
import sys

def system_alt():
    in_conn_display_pipe, out_conn_display_pipe = mp.Pipe()
    in_conn_detect_pipe, out_conn_detect_pipe = mp.Pipe()
    in_conn_faces_pipe, out_conn_faces_pipe = mp.Pipe()
    det_ready_mutex = mp.Lock()
    face_ready_mutex = mp.Lock()

    producer = mp.Process(target=produce_data_alt, args=(in_conn_display_pipe, in_conn_detect_pipe, det_ready_mutex, ))
    producer.start()

    detector = mp.Process(target=detect_faces_alt, args=(out_conn_detect_pipe, in_conn_faces_pipe, det_ready_mutex, face_ready_mutex, ))

    displayer = mp.Process(target=display_alt, args=(out_conn_display_pipe, out_conn_faces_pipe, face_ready_mutex, ))
    displayer.start()

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        time.sleep(0.1)
        sys.exit()
