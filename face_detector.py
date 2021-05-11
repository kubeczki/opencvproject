import cv2
import time
from logger import log, log_process_duration


def detect_faces_std(in_queue, out_queue, faces_queue):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    while True:
        image = in_queue.get()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            1.1,
            4
        )
        faces_queue.put(faces)
        out_queue.put(image)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        process_duration = time.time() - process_start
        log_process_duration("detect_faces_std", process_duration)


def detect_faces_alt(raw_image_pipe_out, processed_image_pipe_in, faces_pipe_in):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    while True:
        image = raw_image_pipe_out.recv()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            1.1,
            4
        )
        faces_pipe_in.send(faces)
        processed_image_pipe_in.send(image)

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    raw_image_pipe_out.close()
    processed_image_pipe_in.close()
    faces_pipe_in.close()


def detect_faces_samp(queue, faces_queue, sampling_step):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    counter = 0
    while True:
        process_start = time.time()
        image = queue.get()
        if counter == 0:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                1.1,
                4
            )
            log(time.asctime(), "detect_faces_samp;", "Face detection on frame completed")
        faces_queue.put(faces)
        counter += 1
        counter %= sampling_step

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
