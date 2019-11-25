import cv2

CAPTURE_SIZE = (640, 480)

# Temporary OpenCV video capture to streamable object test
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_SIZE[0])
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_SIZE[1])

# Load the cascade
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
#face_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def inRect(_face, _rect):
    if _face is not None:
        x1, y1, w1, h1 = _rect
        x2, y2, w2, h2 = _face
        w2 *= 1.5
        h2 *= 1.5
        if x1 + w1/2 > x2 and x1 + w1/2 < x2 + w2:
            if y1 + h1/2 > y2 and y1 + h1 /2 < y2 + h2:
                return True
    return False

while True:
    ret_val, img = cam.read()
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    #faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    eyes = eye_cascade.detectMultiScale(gray, 1.25, 8)
    face = None
    #if len(faces) > 0:
    #    face = faces[0]
    # Draw rectangle around the faces
    for (x, y, w, h) in eyes:
        #if inRect(face, (x,y,w,h)):
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the output
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
