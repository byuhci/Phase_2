import cv2
import matplotlib
import numpy as np
import imutils
#from skimage import measure
from imutils import contours

# read in the image and make it grey scale.
berry_image = cv2.imread("berry_picture_light.jpg",)

print("Detecting berries....")

berry_image_gray = cv2.cvtColor(berry_image, cv2.COLOR_BGR2GRAY)

###############
#cv2.imshow("berry_image_gray", berry_image_gray)
#cv2.waitKey(0)
###############

# blurrs the image so that you can get cleaner points to work with.
berry_image_blurred = cv2.GaussianBlur(berry_image, (7,7), 0)

#cv2.imshow("berry_image_gray", berry_image_blurred)
#cv2.waitKey(0)

berry_image_hsv = cv2.cvtColor(berry_image_blurred, cv2.COLOR_BGR2HSV)



#cv2.imshow("berry_image_gray", berry_image_hsv)
#cv2.waitKey(0)

#parameters for the mask.
def hsv_color_params(color):
    lower_hue = []
    upper_hue = []
    if color == 'black':
        lower_hue = np.array([0,0,0])
        upper_hue = np.array([255,200,80])
    elif color == 'white':
        lower_hue = np.array([0,0,0])
        upper_hue = np.array([0,0,255])
    return lower_hue, upper_hue

chosen_color = 'black'
lower_hue,upper_hue = hsv_color_params(chosen_color)


black_mask = cv2.inRange(berry_image_hsv, lower_hue, upper_hue)




# initialized the detector with no parameters
detector_params = cv2.SimpleBlobDetector_Params()
detector = cv2.SimpleBlobDetector_create(detector_params)


# detect the blobs in the image.

#berries = detector.detect(black_mask)

berries_thresh_erode = cv2.erode(black_mask, None, iterations = 2)
#cv2.imshow("Eroded", berries_thresh_erode)
berries_thresh_dilate = cv2.dilate(berries_thresh_erode, None, iterations = 9)

#berries = detector.detect(berries_thresh_dilate)
_, contours, hierarchy = cv2.findContours(berries_thresh_dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

berry_id = 0
contour_list = []
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 5000 and area < 32000:
        berry_id = berry_id + 1
        contour_list.append(contour)
        M = cv2.moments(contour)
        cX = int(M["m10"]/M["m00"])
        cY = int(M["m01"]/M["m00"])

        cv2.putText(berry_image, "Berry {}".format(berry_id), (cX,cY-80), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255),2)

#cv2.imshow("Berries", berries_thresh_dilate)

print(berry_id," berries detected in image!")
"""
def draw_berry_contours(image):
    cntrs = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntrs = cntrs[0] if imutils.is_cv2() else cntrs[1]
    cntrs = contours.sort_contours(cntrs)[0]

    for (i,c) in enumerate(cntrs):
        (x, y , w, h) = cv2.boundingRect(c)
        ((cX,cY)), radius = cv2.minEnclosingCircle((c), (0,0,255),2)
        cv2.putText(image,"Berry #{}".format(i+1), (x,y-15), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.45, (0,255,0),2)



draw_berry_contours(berries_thresh_dilate)
cv2.waitKey(0)
"""
#detective = cv2.FastFeatureDetector_create("LIGHT SEEKER")
#descriptor = cv2.DescriptorExtractor_create("LIGHT SEEKER")

# Hue range for looking for a green led in the image

(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(berry_image_gray)
cv2.circle(berry_image, maxLoc, 5, (255,0,0), 2)
cv2.imshow("", berry_image)
"""
detect = detective.detect(berry_image)

berry_image_keypoints = berry_image
indicator_light_detected = cv2.drawKeypoints(berry_image, detect, np.array([]),(0,255,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("keypoints", indicator_light_detected)
"""
#berry_image = cv2.bitwise_not(berry_image)

#image_with_detected_berries = cv2.drawKeypoints(berry_image, berries, np.array([]), (255,0 ,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.drawContours(berry_image,contour_list, -1,(0,255,0),2)
# show the points that are detected
cv2.imshow("Detected Berries", berry_image)
print("")
print("Click on a berry to start programming!")
print("")
#cv2.imshow("Detected Berries", image_with_detected_berries)

def mouse_click_event(event, x, y, flags, params):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #cv2.circle(berry_image,(x,y), 100, (255,0,0),-1)
        lo = cv2.getTrackbarPos('lo', 'floodfill')
        hi = cv2.getTrackbarPos('hi', 'floodfill')

        cv2.floodFill(berry_image, berries_thresh_dilate, None, (255,255,255), )
        mouseX,mouseY = x,y
cv2.setMouseCallback("Detected Berries", mouse_click_event)

while(1):
    #cv2.imshow("clickable", berry_image)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(mouseX,mouseY)

cv2.waitKey(0)