# Third party imports
import cv2
import time
import numpy as np

captureSize = (640, 320)
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, captureSize[0])
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, captureSize[1])

# Camera warmup
#time.sleep(1)

# Settings
sensitivity = 10
bgSubThreshold = 30

bgSubtractor = cv2.createBackgroundSubtractorMOG2(10, bgSubThreshold)

def bgSubMasking(bgSubtractor, frame, Lr):
        fgmask = bgSubtractor.apply(frame, learningRate=Lr)
        kernel = np.ones((4, 4), np.uint8)
        # MORPH_OPEN removes noise
        # MORPH_CLOSE closes the holes in the object
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=2)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel, iterations=4)
        return cv2.bitwise_and(frame, frame, mask=fgmask)

for i in range(60):
    # Retrieve background image
    ret, bgFrame = cam.read()
    # Convert to HSV colour space
    bgFrame = bgSubMasking(bgSubtractor, bgFrame, .99)

CV_CAP_PROP_BRIGHTNESS      = cam.get(cv2.CAP_PROP_BRIGHTNESS)
CV_CAP_PROP_CONTRAST        = cam.get(cv2.CAP_PROP_CONTRAST)
CV_CAP_PROP_SATURATION      = cam.get(cv2.CAP_PROP_SATURATION)
CV_CAP_PROP_EXPOSURE        = cam.get(cv2.CAP_PROP_EXPOSURE)
CV_CAP_PROP_GAIN            = cam.get(cv2.CAP_PROP_GAIN)
#CV_CAP_PROP_WHITE_BALANCE_U = cam.get(cv2.CAP_PROP_WHITE_BALANCE_U)
#CV_CAP_PROP_WHITE_BALANCE_V = cam.get(cv2.CAP_PROP_WHITE_BALANCE_V)

while True:
    
    cam.set(cv2.CAP_PROP_BRIGHTNESS, CV_CAP_PROP_BRIGHTNESS)
    cam.set(cv2.CAP_PROP_CONTRAST, CV_CAP_PROP_CONTRAST)
    cam.set(cv2.CAP_PROP_SATURATION, CV_CAP_PROP_SATURATION)
    cam.set(cv2.CAP_PROP_EXPOSURE, CV_CAP_PROP_EXPOSURE)
    cam.set(cv2.CAP_PROP_GAIN, CV_CAP_PROP_GAIN)
    #cam.set(cv2.CAP_PROP_WHITE_BALANCE_U, CV_CAP_PROP_WHITE_BALANCE_U)
    #cam.set(cv2.CAP_PROP_WHITE_BALANCE_V, CV_CAP_PROP_WHITE_BALANCE_V)

    ret, frame = cam.read()

    print(str(frame.size))

    frame = bgSubMasking(bgSubtractor, frame, 0)

    #frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    """
    mask = abs(frameHSV-bgFrame)
    #one = np.ones(mask.shape, dtype=np.uint8)
    #out = np.zeros(mask.shape, dtype=np.uint8)
    #out = one[mask[:,:,0]+mask[:,:,1] < sensitivity]
    out = np.where(mask[:,:,0]+mask[:,:,1]+mask[:,:,2] < sensitivity, 0, 1)
    #out = 0 if mask[:,:,0]+mask[:,:,1] < sensitivity else 1
    #print("out:" + str(out.shape))
    #print("mask:" + str(mask.shape))
    #print("frameHSV:" + str(frameHSV.shape))
    #frameHSV = cv2.bitwise_and(frameHSV, frameHSV, mask=out)
    frameHSV[:,:,0] = frameHSV[:,:,0] * out[:,:]
    frameHSV[:,:,1] = frameHSV[:,:,1] * out[:,:]
    frameHSV[:,:,2] = frameHSV[:,:,2] * out[:,:]

    #frameHSV[:,:] = np.where(abs(frameHSV[:,:,0]-bgFrame[:,:,0]) + abs(frameHSV[:,:,1]-bgFrame[:,:,1]) > sensitivity, frameHSV[:,:], [0,0,0])
    #[0,0,0] if frameHSV[:,:,0] > bgFrame[:,:,0] + sensitivity else frameHSV[:,:]
    #frame = cv2.bitwise_xor(frameHSV, bgFrame)
    #for y in range(captureSize[1]):
    #    for x in range(captureSize[0]):
    #        if inSensitivityRange(bgFrame[y,x,0], frameHSV[y,x,0], sensitivity) and inSensitivityRange(bgFrame[y,x,1], frameHSV[y,x,1], sensitivity):
    #            frameHSV[y,x] = [0,0,0]
    """
    #frame = cv2.cvtColor(frameHSV, cv2.COLOR_HSV2BGR)

    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# Cleanup
cv2.destroyAllWindows()
cam.release()