import multiprocessing as mp
from data_producer import produce_data_samp
from image_modifier import modify_samp, display_samp
from face_detector import detect_faces_samp
import cv2
import time
import sys


def system_sampling():
    # producer - raw_input
    raw_image_pipe_in, raw_image_pipe_out = mp.Pipe()
    # list of detected faces
    raw_image_det_pipe_in, raw_image_det_pipe_out = mp.Pipe()
    # facee locations
    faces_in, faces_out = mp.Pipe()
    # modified parts of images
    modified_image_pipe_in, modified_image_pipe_out = mp.Pipe()


    producer = mp.Process(target=produce_data_samp, args=(raw_image_pipe_in, raw_image_det_pipe_in, ))
    producer.start()

    modifier = mp.Process(target=modify_samp, args=(raw_image_det_pipe_out, faces_in, modified_image_pipe_in, ))
    modifier.start()

    displayer = mp.Process(target=display_samp, args=(raw_image_pipe_out, modified_image_pipe_out, faces_out, ))
    displayer.start()

    producer.join()
    modifier.join()
    displayer.join()

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        sys.exit()
