import multiprocessing as mp
from data_producer import produce_data_std
from image_modifier import modify_std
from face_detector import detect_faces_std


def system_std(file_name, resolution):
    raw_input_queue = mp.Queue()
    processed_queue = mp.Queue()
    faces_queue = mp.Queue()
    time_control = mp.Queue()

    producer = mp.Process(target=produce_data_std, args=(raw_input_queue, time_control, file_name, resolution, ))
    producer.start()

    detector = mp.Process(target=detect_faces_std, args=(raw_input_queue, processed_queue, faces_queue, ))
    detector.start()

    displayer = mp.Process(target=modify_std, args=(processed_queue, faces_queue, time_control, ))
    displayer.start()

    producer.join()
    detector.join()
    displayer.join()

