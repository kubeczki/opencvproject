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


def blur_extract(image, x, y, w, h):
    face_rect = (x, y, x+w, y+h)
    image = cv2_to_pil(image)
    face = image.crop(face_rect)
    face = pil_to_cv2(face)
    kernel_w = int(w / 2)
    kernel_h = int(h / 2)
    if kernel_w % 2 == 0:
        kernel_w -= 1
    if kernel_h % 2 == 0:
        kernel_h -= 1
    return cv2.GaussianBlur(face, (kernel_w, kernel_h), 0)


def paste_blurred_fragment(image, fragment, x, y, w, h):
    face = (x, y, x+w, y+h)
    result = cv2_to_pil(image)
    fragment = cv2_to_pil(fragment)
    result.paste(fragment, face)
    return pil_to_cv2(result)


def modify_samp(raw_image_det_pipe_out, faces_pipe_in, modified_image_pipe_in):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    while True:
        image = raw_image_det_pipe_out.recv()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            1.1,
            4
        )
        extract = image
        for (x, y, w, h) in faces:
            extract = blur_extract(image, x, y, w, h)
        modified_image_pipe_in.send(extract)
        faces_pipe_in.send(faces)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    raw_image_det_pipe_out.close()
    faces_pipe_in.close()
    modified_image_pipe_in.close()


def display_samp(raw_image_pipe_out, modified_image_pipe_out, faces_pipe_out):
    cv2.namedWindow('image_display', cv2.WINDOW_AUTOSIZE)
    mode = 1
    start_time = time.time()
    number_of_seconds = 1
    counter = 0
    fps = "FPS: "
    while True:
        image = raw_image_pipe_out.recv()
        extract = modified_image_pipe_out.recv()
        faces = faces_pipe_out.recv()

        for (x, y, w, h) in faces:
            if mode < 0:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                # error
                image = paste_blurred_fragment(image, extract, x, y, w, h)
        counter += 1
        if (time.time() - start_time) > number_of_seconds:
            fps = "FPS: "
            fps += str(round(counter / (time.time() - start_time)))
            counter = 0
            start_time = time.time()
        cv2.putText(image, fps, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('image_display', image)

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            break
        elif k == 32:
            mode *= -1

    raw_image_pipe_out.close()
    modified_image_pipe_out.close()
