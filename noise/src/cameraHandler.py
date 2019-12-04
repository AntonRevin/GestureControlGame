"""
    src.camerahandler
    OpenCV
"""

# Third party imports
import cv2
import numpy as np

# Local imports

class CameraHandler:
    # Object constructor
    def __init__(self, captureSize):
        # Store variables
        self.captureSize = captureSize
        self.cam = None
        self.bgSubtractor = cv2.createBackgroundSubtractorMOG2(10, 30)
        self.bgCalibrated = False
        self.frame = None

    def startCameraStream(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.captureSize[0])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.captureSize[1])

    def bgSubMasking(self, frame, Lr):
        fgmask = self.bgSubtractor.apply(frame, learningRate=Lr)
        kernel = np.ones((4, 4), np.uint8)
        # MORPH_OPEN removes noise
        # MORPH_CLOSE closes the holes in the object
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=2)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel, iterations=4)
        return cv2.bitwise_and(frame, frame, mask=fgmask)

    def calibrateBackground(self, calibrationPeriod): 
        for i in range(calibrationPeriod):
            # Retrieve background image
            ret, bgFrame = self.cam.read()
            # Learn background information
            bgFrame = self.bgSubMasking(bgFrame, .95)
        
        # Save camera properties
        self.CV_CAP_PROP_BRIGHTNESS  = self.cam.get(cv2.CAP_PROP_BRIGHTNESS)
        self.CV_CAP_PROP_CONTRAST    = self.cam.get(cv2.CAP_PROP_CONTRAST)
        self.CV_CAP_PROP_SATURATION  = self.cam.get(cv2.CAP_PROP_SATURATION)
        self.CV_CAP_PROP_EXPOSURE    = self.cam.get(cv2.CAP_PROP_EXPOSURE)
        self.CV_CAP_PROP_GAIN        = self.cam.get(cv2.CAP_PROP_GAIN)

        self.bgCalibrated = True

    def fetchFrame(self):
        # Maintain constant camera properties
        if self.bgCalibrated:
            self.cam.set(cv2.CAP_PROP_BRIGHTNESS,   self.CV_CAP_PROP_BRIGHTNESS)
            self.cam.set(cv2.CAP_PROP_CONTRAST,     self.CV_CAP_PROP_CONTRAST)
            self.cam.set(cv2.CAP_PROP_SATURATION,   self.CV_CAP_PROP_SATURATION)
            self.cam.set(cv2.CAP_PROP_EXPOSURE,     self.CV_CAP_PROP_EXPOSURE)
            self.cam.set(cv2.CAP_PROP_GAIN,         self.CV_CAP_PROP_GAIN)

        # Fetch next frame
        ret, self.frame = self.cam.read()

        # Remove background
        if self.bgCalibrated:
            self.frame = self.bgSubMasking(self.frame, 0)