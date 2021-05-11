import numpy as np
import cv2
import time
from PIL import Image
from logger import log, log_delay, log_process_duration


def cv2_to_pil(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


def pil_to_cv2(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def blur_fragment(image, x, y, w, h):
    fragment = (x, y, x + w, y + h)
    image = cv2_to_pil(image)
    extracted = image.crop(fragment)
    extracted = pil_to_cv2(extracted)
    kernel_w = int(w / 2)
    kernel_h = int(h / 2)
    if kernel_w % 2 == 0:
        kernel_w -= 1
    if kernel_h % 2 == 0:
        kernel_h -= 1
    extracted = cv2.GaussianBlur(extracted, (kernel_w, kernel_h), 0)
    extracted = cv2_to_pil(extracted)
    image.paste(extracted, fragment)
    return pil_to_cv2(image)


# store the blurred face in the output image
def modify_std(queue, faces_queue, time_queue):
    # create window
    cv2.namedWindow('image_display', cv2.WINDOW_AUTOSIZE)
    start_time = time.time()
    mode = 1
    number_of_seconds = 1
    frame_number = 0
    counter = 0
    fps = "FPS: "
    while True:
        process_start = time.time()
        image = queue.get()
        faces = faces_queue.get()
        for (x, y, w, h) in faces:
            if mode < 0:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                image = blur_fragment(image, x, y, w, h)
        counter += 1
        if (time.time() - start_time) > number_of_seconds:
            fps = "FPS: "
            fps += str(round(counter / (time.time() - start_time)))
            counter = 0
            start_time = time.time()
        cv2.putText(image, fps, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('image_display', image)

        time_since_captured = time_queue.get()
        difference = time.time() - time_since_captured
        frame_number += 1

        log_delay(frame_number, difference)
        log(time.asctime(), "modify_std;", "Effect applied and image shown")

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            break
        elif k == 32:
            mode *= -1

        process_duration = time.time() - process_start
        log_process_duration("modify_std", process_duration)


def modify_alt(processed_image_pipe_out, faces_pipe_out, time_control_pipe_out):
    # create window
    cv2.namedWindow('image_display', cv2.WINDOW_AUTOSIZE)
    start_time = time.time()
    mode = 1
    number_of_seconds = 1
    counter = 0
    frame_number = 0
    fps = "FPS: "
    while True:
        process_start = time.time()
        image = processed_image_pipe_out.recv()
        faces = faces_pipe_out.recv()
        for (x, y, w, h) in faces:
            if mode < 0:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                image = blur_fragment(image, x, y, w, h)
        counter += 1
        if (time.time() - start_time) > number_of_seconds:
            fps = "FPS: "
            fps += str(round(counter / (time.time() - start_time)))
            counter = 0
            start_time = time.time()
        cv2.putText(image, fps, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('image_display', image)

        time_since_captured = time_control_pipe_out.recv()
        difference = time.time() - time_since_captured
        frame_number += 1

        log_delay(frame_number, difference)
        log(time.asctime(), "modify_alt;", "Effect applied and image shown")

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            break
        elif k == 32:
            mode *= -1

        process_duration = time.time() - process_start
        log_process_duration("modify_alt", process_duration)

    time_control_pipe_out.close()
    processed_image_pipe_out.close()
    faces_pipe_out.close()


def modify_samp(queue, faces_queue, time_control_queue):
    # create window
    cv2.namedWindow('image_display', cv2.WINDOW_AUTOSIZE)
    start_time = time.time()
    mode = 1
    number_of_seconds = 1
    counter = 0
    frame_number = 0
    fps = "FPS: "
    while True:
        process_start = time.time()
        image = queue.get()
        faces = faces_queue.get()
        for (x, y, w, h) in faces:
            if mode < 0:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                image = blur_fragment(image, x, y, w, h)
        counter += 1
        if (time.time() - start_time) > number_of_seconds:
            fps = "FPS: "
            fps += str(round(counter / (time.time() - start_time)))
            counter = 0
            start_time = time.time()
        cv2.putText(image, fps, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('image_display', image)

        time_since_captured = time_control_queue.get()
        difference = time.time() - time_since_captured
        frame_number += 1

        log_delay(frame_number, difference)
        log(time.asctime(), "modify_samp;", "Effect applied and image shown")

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            break
        elif k == 32:
            mode *= -1

        process_duration = time.time() - process_start
        log_process_duration("modify_samp", process_duration)