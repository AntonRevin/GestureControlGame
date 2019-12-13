import numpy as np
import cv2
from scipy import spatial
 
# Cargamos la imagen
original = cv2.imread("hand3.jpg")
original_2 = original.copy()
height = np.size(original, 0)
width = np.size(original, 1)
#cv2.imshow("original", original)
print("height: ", height, "width: ", width)
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

# create hull array for convex hull points
hull = []
hull_defects = []
#vertices = []
 
# calculate points for each contour
for i in range(len(contornos)):
    # creating convex hull object for each contour
    hull.append(cv2.convexHull(contornos[i]))#, returnPoints= False))
    hull_defects.append(cv2.convexHull(contornos[i], returnPoints= False))
#vertices.append(hull[i].vertices)

#print ("number of vertices detected: ", len(vertices))

#hull_indices = hull.vertices

"""
# compute the center of the contour
M = cv2.moments(canny)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
"""



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

"""
for i in range(len(hull)):
    cv2.fillConvexPoly(, hull[i], (255, 255, 255))

cv2.imshow("fill_hull", original)
"""

#minimum ratio circle around hand
max_radius = 0
center_max = 0
largest_hull = 0
for i in range(len(hull)):
    (x,y),radius = cv2.minEnclosingCircle(hull[i])
    center = (int(x),int(y))
    radius = int(radius)
    if max_radius < radius:
        max_radius = radius
        largest_hull = hull[i]
        largest_hull_defects = hull_defects[i]
        center_max = center

real_largest_hull = [largest_hull]

cv2.circle(original, center_max, max_radius, (255, 255, 255), 3)
black_image = np.zeros((height,width))
white_image = np.ones((height,width))
probe_image = np.zeros((height,width))

cv2.fillConvexPoly(white_image, largest_hull, (0, 0, 0))

hand_conts = []

convex_point = 0

#This fuckin function is supposed to count the contour convex but idk
#why it doesnt recognize the convex points on the hand 

for i in range(len(hand_conts)):
    if cv2.isContourConvex(hand_conts[i]) == True:
        convex_point = convex_point + 1

print ("number of contours detected: ", len(contornos))
print ("number of convex_points: ", convex_point)


howmany = 0

for i in range(len(contornos)):
    """cont = contornos[i]
    pnt = cont[0][0]
    point = (pnt[0], pnt[1])
    if cv2.pointPolygonTest(largest_hull,point,False) == 1:
        fuck_contours = [contornos[i]]
        cv2.drawContours(black_image, fuck_contours, -1, (255, 255, 255), 1, 8)"""
    cont = contornos[i]
    inside = False
    for pnt in cont:
        pnt = pnt[0]
        point = (pnt[0], pnt[1])
        if cv2.pointPolygonTest(largest_hull,point,False) == 1:
            inside = True
    if inside:
        #cv2.fillPoly(black_image, [cont], (255, 255, 255))
        #cv2.fillPoly(black_image, cont, (255, 255, 255))
        #cv2.drawContours(white_image, [cont], -1, (0,0,0),thickness=-1)
        cv2.drawContours(black_image, [cont], -1, (255,255,255),thickness=-1)

        """fuck_contours = [cont]
        cv2.drawContours(black_image, fuck_contours, -1, (255, 255, 255), 1, 8)"""
        hand_conts.append(cont)
        howmany += 1

print("There are " + str(howmany) + " contours in the hand.")

k = cv2.getStructuringElement(cv2.MORPH_CROSS,(30,30))
closing = cv2.morphologyEx(black_image, cv2.MORPH_CLOSE, k)
cv2.imshow("closed_img", closing)

"""
(contornos_cerrados,_)= cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(contornos_cerrados)):
    cv2.fillPoly(probe_image, contornos_cerrados[i], (255,255,255))
    """

#cv2.fillPoly(black_image, [hand_conts[1]], (255,255,255))

#cv2.drawContours(black_image, fuck_contours, -1, (255, 255, 255), 1, 8)

# draw contours and hull points

wh = 1
number_points = 0
defects = cv2.convexityDefects(hand_conts[wh],largest_hull_defects)

for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    #start = tuple(hand_conts[wh][s][0])
    #end = tuple(hand_conts[wh][e][0])
    far = tuple(hand_conts[wh][f][0])
    dist = cv2.pointPolygonTest(largest_hull,far,False)
    #print("Dist [" + str(i)+"]: " + str(dist))
    #cv2.line(original,start,end,[0,0,255],2)
    if dist == 0:
        number_points=number_points+1
        cv2.circle(original,far,5,[0,0,255],-1)

print("There are " + str(number_points) + " recognized points.")
if (number_points >= 5):
    print("PAPER")
    cv2.putText(original, "PAPER", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0 ,0 ,0), 2)
"""
for i in range(height):
    for j in range(width):
        if(cv2.pointPolygonTest(hand_conts[1],(j,i),False)== -1):
            probe_image[i,j] = 1
"""
#and cv2.pointPolygonTest(hand_conts[0],(j,i),False)==-1


# draw ith convex hull object
cv2.drawContours(original, real_largest_hull, -1, (255, 0, 0), 1, 8)
cv2.drawContours(original_2, hull, -1, (255, 0, 0), 1, 8)
#cv2.drawContours(BW, hull, -1, (255, 0, 0), 1, 8)
# draw the contour and center of the shape on the image
#cv2.circle(original, (cX, cY), 7, (255, 255, 255), -1)
cv2.drawContours(original, hand_conts, -1, (0, 255, 0), 2)
# draw the aprroximated contour 
cv2.drawContours(original_2, approx, -1, (0, 255, 0), 2)
#cv2.drawContours(BW, contornos, -1, (255, 255, 255), 2)

"""
#Tried to fill contour
cv2.drawContours(canny, [max(contornos, key = cv2.contourArea)], -1, 255, thickness=-1)
 """   
cv2.drawContours(probe_image, real_largest_hull, -1, (255, 0, 0), 1, 8)

cv2.imshow("contours", original)
#cv2.imshow("approximated contours", original_2)
#cv2.imshow("alone shapes", black_image)
#cv2.imshow("try", BW)
cv2.imshow("hand_contour", black_image)
cv2.imshow("filled_hull", white_image)
cv2.imshow("hull", probe_image)

cv2.waitKey(0)

"""
I have two ideas. First, try to analyse the hull shape and look for
changes on the direction. Second, do a mask that only let see the pixels
between the hull and the contour.
"""