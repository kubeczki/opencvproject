import cv2


def detect_faces(in_queue, out_queue, faces_queue):
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

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break


def detect_faces_alt(detection_connection, faces_connection, detection_mutex, faces_mutex):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')