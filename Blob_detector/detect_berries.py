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

# blurrs the image so that you can get cleaner points to work with.
berry_image_blurred = cv2.GaussianBlur(berry_image, (7,7), 0)

berry_image_hsv = cv2.cvtColor(berry_image_blurred, cv2.COLOR_BGR2HSV)

#parameters for the mask, filter out black objects from white objects to detect the berries.
#simplist way to do this against a black background.
def hsv_color_params(color):
    lower_hue = []
    upper_hue = []
    if color == 'black':
        lower_hue = np.array([0,0,0])
        upper_hue = np.array([255,100,85])
    elif color == 'white':
        lower_hue = np.array([0,0,0])
        upper_hue = np.array([0,0,255])
    return lower_hue, upper_hue

def compare(image1,image2):
    original = image1
    light = image2

    difference_between_images = cv2.subtract(image1,image2,)
    return difference_between_images


chosen_color = 'black'
lower_hue,upper_hue = hsv_color_params(chosen_color)

black_mask = cv2.inRange(berry_image_hsv, lower_hue, upper_hue)

# initialized the detector with no parameters
detector_params = cv2.SimpleBlobDetector_Params()
detector = cv2.SimpleBlobDetector_create(detector_params)

berries_thresh_erode = cv2.erode(black_mask, None, iterations = 2)

berries_thresh_dilate = cv2.dilate(berries_thresh_erode, None, iterations = 9)


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

#detective = cv2.FastFeatureDetector_create("LIGHT SEEKER")
#descriptor = cv2.DescriptorExtractor_create("LIGHT SEEKER")

# bright spot for looking for a green led in the image, will catch reflections.
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(berry_image_gray)
cv2.circle(berry_image, maxLoc, 5, (255,0,0), 2)
cv2.imshow("", berry_image)

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