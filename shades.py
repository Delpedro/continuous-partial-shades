import cv2
import sys
import os

debug = (os.environ.get('DEBUG') == '1')

# Get user supplied values
image_path = sys.argv[1]

# Create the haar cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

shades = cv2.imread("shades.png")

# Read the image
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags=cv2.CASCADE_SCALE_IMAGE
)

print("Found {0} faces!".format(len(faces)))

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    if debug:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    roi_gray = gray[y:y+h, x:x+w]
    roi_color = image[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)

    print("Found {0} eyes!".format(len(eyes)))

    if len(eyes) == 2:
        shades_h = shades.shape[0]
        shades_w = shades.shape[1]
        new_shades_w = w
        new_shades_h = int(w * (shades_h/shades_w))

        shades_x = 0
        shades_center_y = (eyes[0][1] + eyes[0][3]/2 + eyes[1][1] + eyes[1][3]/2)/2
        shades_y = shades_center_y - new_shades_h/2

        resized_shades = cv2.resize(shades, (new_shades_w, new_shades_h))
        roi_color[shades_y:shades_y+new_shades_h, shades_x:new_shades_w] = resized_shades

    if debug:
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)


cv2.imwrite("out.jpg", image)
