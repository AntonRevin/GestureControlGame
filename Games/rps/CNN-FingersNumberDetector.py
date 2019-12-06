import cv2
import math
import numpy as np

import os



class FingersNumberDetector:
    def histMasking(frame, handHist):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0, 1], handHist, [0, 180, 0, 256], 1)
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
        cv2.filter2D(dst, -1, disc, dst)
        # dst is now a probability map
        # Use binary thresholding to create a map of 0s and 1s
        # 1 means the pixel is part of the hand and 0 means not
        ret, thresh = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=7)
        thresh = cv2.merge((thresh, thresh, thresh))
        return cv2.bitwise_and(frame, thresh)

        histMask = histMasking(roi, handHist)
        bgSubMask = bgSubMasking(roi)
        mask = cv2.bitwise_and(histMask, bgSubMask)

    def threshold( mask):
        grayMask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(grayMask, 0, 255, 0)
        return thresh

    def getMaxContours(self, contours):
        maxIndex = 0
        maxArea = 0

        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)

            if area > maxArea:
                maxArea = area
                maxIndex = i
        return contours[maxIndex]

    thresh = threshold(mask)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # There might be no contour when hand is not inside the frame

    if len(contours) > 0:
        maxContour = getMaxContours(contours)


    def countFingers(contour):
        hull = cv2.convexHull(contour, returnPoints=False)
        if len(hull) > 3:
            defects = cv2.convexityDefects(contour, hull)
            cnt = 0
            if type(defects) != type(None):
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(contour[s, 0])
                    end = tuple(contour[e, 0])
                    far = tuple(contour[f, 0])
                    angle = calculateAngle(far, start, end)
                
                    # Ignore the defects which are small and wide
                    # Probably not fingers
                    if d > 10000 and angle <= math.pi/2:
                        cnt += 1
            return True, cnt
        return False, 0
    
    def calculateAngle(far, start, end):
        """Cosine rule"""
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2) / (2*b*c))
        return angle

