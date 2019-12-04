# USAGE
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat

# SRC: https://www.pyimagesearch.com/2017/04/10/detect-eyes-nose-lips-jaw-dlib-opencv-python/

# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import imutils
import time
import dlib
import cv2

from src.utilities import slidingAverage, mean
 
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("predictor.dat")

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream().start()
time.sleep(1.0)

# Smoothing variables
_deltaXHistory = []
_deltaYHistory = []
_deltaX = 0
_deltaY = 0
smoothingLevel = 4

# Constants
DEADZONE = 4

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
	rects = detector(gray, 0)
	
	# If face detected
	if len(rects) > 0:
		rect = rects[0]

		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		""" 
		# Draw facial tracking points
		for (x, y) in shape:
			cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
		"""

		(x1,y1) = shape[30] # Tip of nose
		(x2,y2) = shape[29] # Nose point 2
		(x3,y3) = shape[28] # Nose point 3
		(x4,y4) = shape[27] # Top of nose
		(t,y2) = shape[1] 	# Left ear
		(t,y3) = shape[15]	# Right ear
		avgx = mean([x1, x2, x3, x4])
		deltax = x1 - avgx
		avgy = mean([y2, y3])
		deltay = y1 - (avgy)*1.02
		# Perform smoothing
		_deltaX, _deltaXHistory = slidingAverage(_deltaXHistory, deltax, smoothingLevel)
		_deltaY, _deltaYHistory = slidingAverage(_deltaYHistory, deltay, smoothingLevel)
		# Draw direction arrow
		cv2.arrowedLine(
			frame, (x1,y1), 
			(int(x1 + _deltaX * 16), 
			int(y1 + (_deltaY)*4)), 
			(255,0,0), 
			thickness=5, 
			tipLength=0.25
		)

		# Draw prediction
		pred = "FORWARD"
		q = 4 * abs(_deltaX / _deltaY)
		if _deltaX < - DEADZONE / 4:
			if q > 1:
				pred = "RIGHT"
		if _deltaX > DEADZONE / 4:
			if q > 1:
				pred = "LEFT"
		if _deltaY < - DEADZONE:
			if q < 1:
				pred = "UP"
		if _deltaY > DEADZONE:
			if q < 1:
				pred = "DOWN"
		cv2.putText(frame, pred, (0, 26), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()