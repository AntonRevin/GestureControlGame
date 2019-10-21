"""
    src.camerahandler
    OpenCV
"""

# Third party imports
import cv2

# Local imports
from src.utilities import slidingAverage, mean

class CameraHandler:

    # Object constructor
    def __init__(self, captureSize, lowerBoundary, upperBoundary, openingKernel, closingKernel):
        # Store variables
        self.captureSize = captureSize
        self.lowerBoundary = lowerBoundary
        self.upperBoundary = upperBoundary
        self.openingKernel = openingKernel
        self.closingKernel = closingKernel
        self.cam = None
        self.history = []

    def startCameraStream(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.captureSize[0])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.captureSize[1])

    def findControlHeight(self, screenHeight):
        # Fetch camera input and rescale it
        ret, img = self.cam.read()
        img = cv2.resize(img, (240, 120))

        # Convert to HSV colour space
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Create mask based upon upper and lower boundary
        mask = cv2.inRange(imgHSV, self.lowerBoundary, self.upperBoundary)

        # Perform morphological operations (image cleanup)
        maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.openingKernel)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, self.closingKernel)
        maskFinal = maskClose

        # Find the countours around the appropriately coloured regions
        conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Find the smallest upright bounding rectangle around the found contours
        newHeight = -1
        if len(conts) > 0:
            x, y, w, h = cv2.boundingRect(conts[0])
            newHeight = (y + (h/2)) * (screenHeight/120) - 64

        # Perform sliding average on last 4 values for
        if newHeight != -1:
            value, self.history = slidingAverage(self.history, newHeight, 4)
        else:
            value = mean(self.history)

        # Return relative screenspace height
        return value
