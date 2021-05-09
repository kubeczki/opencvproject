import numpy as np
import cv2


# store the blurred face in the output image
def display(queue, faces_queue):
    # create window
    cv2.namedWindow('image_display', cv2.WINDOW_AUTOSIZE)
    while True:
        image = queue.get()
        # faces = faces_queue.get()
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('image_display', image)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            break


def display_alt(display_connection, faces_connection, faces_mutex):
    # create window
    cv2.namedWindow('image_display', cv2.WINDOW_AUTOSIZE)
    while True:
        image = processed_image_pipe_out.recv()
        faces = faces_pipe_out.recv()
        for (x, y, w, h) in faces:
            if mode < 0:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                image = blur_fragment(image, x, y, w, h)
        cv2.imshow('image_display', image)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            break

    processed_image_pipe_out.close()
    faces_pipe_out.close()
