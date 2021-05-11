import multiprocessing as mp
from data_producer import produce_data_samp
from image_modifier import modify_samp
from face_detector import detect_faces_samp


def system_sampling(sampling_step, file_name):
    raw_input_queue = mp.Queue(1)
    detection_queue = mp.Queue(1)
    faces_queue = mp.Queue(1)
    time_control_queue = mp.Queue(2)

    producer = mp.Process(target=produce_data_samp, args=(raw_input_queue, detection_queue, time_control_queue, file_name, ))
    producer.start()

    detector = mp.Process(target=detect_faces_samp, args=(detection_queue, faces_queue, sampling_step, ))
    detector.start()

    displayer = mp.Process(target=modify_samp, args=(raw_input_queue, faces_queue, time_control_queue, ))
    displayer.start()

    producer.join()
    detector.join()
    displayer.join()

