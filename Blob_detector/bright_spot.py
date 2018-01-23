import cv2
import numpy as np

image = cv2.imread("berry_with_light.jpg")
orig = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
cv2.circle(image, maxLoc, 5, (255,0,0), 2)

cv2.imshow("bright", image)
cv2.waitKey(0)