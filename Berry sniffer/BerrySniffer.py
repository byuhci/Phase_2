'''
Phase 2 berry project
- Detect the PCB outline.
    ~ Find the corners of the outer outline.
    ~ Draw straight lines using the points to get cleans edges.
    ~

- Find all markers and replace them with sensor models.
    ~ Replace tags with a model of the sensor in a preview
    ~ Draw symbol on the PCB layout for the specific sensor

- Draw paths to connect all sensors in a chain.
    ~ Get the orientation from the marker.
    ~ Know where the contacts need to be placed
    ~ Rout the path using XML, not intersecting with the sensors or the perimeter.

- Export as a finished CAD file for making a pcb.
    ~ Finished file should be something usable. (dwg or something similar)
    ~ Export the file with the models of the sensors on the pcb.

'''



import numpy as np
# from PIL import Image
import cv2
import xml.etree.cElementTree as ET
import cv2.aruco


# library for finding the aruco markers.
# aruco_library = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4x4_100)
sniff_library = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)

# load image and shrink - it's massive
img = cv2.imread('test_curve.jpg')
# img = cv2.resize(img, None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
# get a blank canvas for drawing contour on and convert img to gray scale
canvas = np.zeros(img.shape, np.uint8)
# colors the main image gray so it is easier to work with.
img2gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Detection of the markers needs to take place before an more processing can happen.
corners, ids, params = cv2.aruco.detectMarkers(img, sniff_library)
cv2.aruco.drawDetectedMarkers(img, corners,ids)
# filter out small lines
#the float is a data type that is need for the process
kernel = np.ones((5,5),np.float32)/25
img2gray = cv2.filter2D(img2gray,-1,kernel)

# threshold the image and extract contours
ret,thresh = cv2.threshold(img2gray,150,255,cv2.THRESH_BINARY_INV)
thresh = np.invert(thresh)
im2,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


# need to grab the
# image = Image,open()

# find the main island (biggest area)
cnt = contours[0]

max_area = cv2.contourArea(cnt)

for cont in contours:
    if cv2.contourArea(cont) > max_area:
        cnt = cont
        max_area = cv2.contourArea(cont)


# define main island contour approx. and hull
perimeter = cv2.arcLength(cnt,True)
epsilon = 0.002*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)

hull = cv2.convexHull(cnt)

# cv2.isContourConvex(cnt)

# this function returned the outer contour/perimeter but it has a lot of noise.
# it takes the pixel edges so lines are not straight.
# cv2.drawContours(canvas, cnt, -1, (0, 255, 0), 3)

cv2.drawContours(img, [approx], -1, (0, 255, 0), 1)

cv2.polylines(img, approx, True, (0,100,255), 5)


# cv2.drawContours(canvas, hull, -1, (0, 0, 255), 3) # only displays a few points as well.
cv2.imshow("Contour", img)
#cv2.imshow("image", img)
#cv2.imshow("gray", img2gray)

# Export the file into an xml file format for use in eagle.


k = cv2.waitKey(0)
cv2.destroyAllWindows()

