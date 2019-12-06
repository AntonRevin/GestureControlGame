import numpy as np
import cv2
from scipy import spatial
 
# Cargamos la imagen
original = cv2.imread("hand3.jpg")
original_2 = original.copy()
height = np.size(original, 0)
width = np.size(original, 1)
cv2.imshow("original", original)
 
# Convertimos a escala de grises
#imageHSV = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)

# Aplicar suavizado Gaussiano
gauss = cv2.GaussianBlur(original, (5,5), 0)
#cv2.imshow("suavizado", gauss)

gray = cv2.cvtColor(gauss, cv2.COLOR_RGB2GRAY)
(thresh, WB) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
BW = cv2.bitwise_not(WB)
#cv2.imshow("blanconegro", BW)

"""
min_HSV = np.array([0/2, 5*2.55, 25*(2.55)])         #, dtype = "uint8")
max_HSV = np.array([20/2, 15*2.55, 100*2.55])      #, dtype = "uint8")
skinRegionHSV = cv2.inRange(imageHSV, min_HSV, max_HSV)

kernel = np.ones((4,4), np.uint8)
fgmask = cv2.morphologyEx(skinRegionHSV, cv2.MORPH_CLOSE, kernel, iterations=2)

skinHSV = cv2.bitwise_and(original, original, mask = fgmask)
cv2.imshow("skinHSV", skinHSV)
BGR_image = cv2.cvtColor(skinHSV, cv2.COLOR_HSV2BGR)
BW_image = cv2.cvtColor(BGR_image, cv2.COLOR_BGR2GRAY)
 
 """
 
# Detectamos los bordes con Canny
canny = cv2.Canny(BW, 50, 150)
#cv2.imshow("canny", canny)
 
# Buscamos los contornos
(contornos,_)= cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

"""
#hullconvex
hull = cv.convexHull(canny)
cv2.imshow("convex", hull)
"""
""" 
#minimum ratio circle around shape
(x,y),radius = cv.minEnclosingCircle(canny)
center = (int(x),int(y))
radius = int(radius)
cv.circle(original,center,radius,(0,255,0),2)
"""
# create hull array for convex hull points
hull = []
#vertices = []
 
# calculate points for each contour
for i in range(len(contornos)):
    # creating convex hull object for each contour
    hull.append(cv2.convexHull(contornos[i], False))
#vertices.append(hull[i].vertices)

#print ("number of vertices detected: ", len(vertices))

#hull_indices = hull.vertices

"""
# compute the center of the contour
M = cv2.moments(canny)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
"""


convex_point = 0

#This fuckin function is supposed to count the contour convex but idk
#why it doesnt recognize the convex points on the hand 

for i in range(len(contornos)):
    if cv2.isContourConvex(contornos[i]) == True:
        convex_point = convex_point + 1

print ("number of contours detected: ", len(contornos))
print ("number of convex_points: ", convex_point)

biggest_area = 0

for i in range(len(contornos)):
    area = cv2.contourArea(contornos[i])
    if biggest_area < area:
        biggest_area = area
        b_a_position = i

print ("biggest area: ", biggest_area, " and is the area of the contour positioned at: ", b_a_position)

#approximation of the contour curve with less points
epsilon = 0.01*cv2.arcLength(contornos[b_a_position],True)
approx = cv2.approxPolyDP(contornos[b_a_position],epsilon,True)

"""
#Tried of filling the contour  
cv2.fillPoly(canny,contornos[1], (255,255,255))
cv2.imshow("fill_contour", canny)
"""
black_image = np.zeros((height,width))
# draw contours and hull points

# draw ith convex hull object
cv2.drawContours(original, hull, -1, (255, 0, 0), 1, 8)
cv2.drawContours(original_2, hull, -1, (255, 0, 0), 1, 8)
cv2.drawContours(BW, hull, -1, (255, 0, 0), 1, 8)
# draw the contour and center of the shape on the image
#cv2.circle(original, (cX, cY), 7, (255, 255, 255), -1)
cv2.drawContours(original, contornos, -1, (0, 255, 0), 2)
# draw the aprroximated contour 
cv2.drawContours(original_2, approx, -1, (0, 255, 0), 2)
cv2.drawContours(BW, contornos, -1, (255, 255, 255), 2)

"""
#Tried to fill contour
cv2.drawContours(canny, [max(contornos, key = cv2.contourArea)], -1, 255, thickness=-1)
 """   


cv2.imshow("contours", original)
cv2.imshow("approximated contours", original_2)
cv2.imshow("alone shapes", BW)

 
cv2.waitKey(0)

"""
I have two ideas. First, try to analyse the hull shape and look for
changes on the direction. Second, do a mask that only let see the pixels
between the hull and the contour.
"""