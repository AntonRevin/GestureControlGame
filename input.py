
# Third party imports
import cv2

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)

    while True:
        ret_val, img = cam.read()
        
        cv2.imshow("input", img)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
