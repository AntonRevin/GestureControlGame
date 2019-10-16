
# Third party imports
import cv2

if __name__ == "__main__":
    # Create camera stream object
    cam = cv2.VideoCapture(0)
    # Specify camera stream properties
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        # Retrieve new frame
        ret_val, img = cam.read()
        
        # Show the stream
        cv2.imshow("input", img)

        # Exit condition
        if cv2.waitKey(1) == 27:
            break
    
    # Perform OpenCV cleanup
    cv2.destroyAllWindows()
