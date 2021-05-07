import numpy as np
import cv2


def anonymize_face_simple(queue, factor=3.0):
    # automatically determine the size of the blurring kernel based
    # on the spatial dimensions of the input image
    image = queue.get()
    (h, w) = image.shape[:2]
    kW = int(w / factor)
    kH = int(h / factor)
    # ensure the width of the kernel is odd
    if kW % 2 == 0:
        kW -= 1
    # ensure the height of the kernel is odd
    if kH % 2 == 0:
        kH -= 1
    # apply a Gaussian blur to the input image using our computed
    # kernel size
    return cv2.GaussianBlur(image, (kW, kH), 0)


# load image

# extract face box

# call blur function

# store the blurred face in the output image
def display(queue):
    # create window
    cv2.namedWindow('image_display', cv2.WINDOW_AUTOSIZE)
    while True:
        if queue.empty() is False:
            image = queue.get()
            cv2.imshow('image_display', image)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            break
