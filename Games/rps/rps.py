import cv2

"""
good about HSV etc as well: https://becominghuman.ai/real-time-finger-detection-1e18fea0d1d4
"""

# Constants
CAPTURE_SIZE = (640, 480)

# Camera input setup
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_SIZE[0])
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_SIZE[1])

# Variables


while True:
    frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)



    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# Cleanup
cv2.destroyAllWindows()
camera.release()
