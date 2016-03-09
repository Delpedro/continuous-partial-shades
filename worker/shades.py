import cv2

import logging
logger = logging.getLogger(__name__)


def add_shades(in_file, out_file, debug=False):
    logger.debug('Reading {}'.format(in_file))
    image = cv2.imread(in_file)

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

    shades = cv2.imread("shades.png", -1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    logger.debug("Found {0} faces".format(len(faces)))

    for (x, y, w, h) in faces:
        if debug:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        logger.debug("  Found {0} eyes".format(len(eyes)))

        if len(eyes) == 2:
            shades_h = shades.shape[0]
            shades_w = shades.shape[1]
            new_shades_w = w
            new_shades_h = int(w * (shades_h/shades_w))

            shades_x = 0
            shades_center_y = (eyes[0][1] + eyes[0][3]/2 + eyes[1][1] + eyes[1][3]/2)/2
            shades_y = shades_center_y - new_shades_h/2

            logger.debug("    Overlaying shades at {}, {}".format(x+shades_x, y+shades_y))
            overlay(roi_color, shades, x=shades_x, y=shades_y, w=new_shades_w, h=new_shades_h)

        if debug:
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)

    logger.debug('Writing {}'.format(out_file))
    cv2.imwrite(out_file, image)


def overlay(bg, fg, x, y, w, h):
    fg = cv2.resize(fg, (w, h))

    for c in range(0,3):
        bg[y:y+h, x:x+w, c] = \
            fg[:,:,c] * (fg[:,:,3]/255.0) + bg[y:y+h, x:x+w, c] * (1.0 - fg[:,:,3]/255.0)


if __name__ == '__main__':
    import os
    import sys

    add_shades(sys.argv[1], "out.jpg", debug=(os.environ.get('DEBUG') == '1'))
