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


def detect_faces_alt(raw_image_pipe_out, processed_image_pipe_in, faces_pipe_in):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while True:
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    raw_image_pipe_out.close()
    processed_image_pipe_in.close()
    faces_pipe_in.close()
