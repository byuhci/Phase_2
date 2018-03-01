from cv2 import *
import numpy as np


#global berry_box_contour_list


def berry_detection():
    contour_list = []

    berry_image = cv2.imread("berry_picture.jpg")

    berry_image_copied = berry_image

    print("Detecting berries....")

    berry_image_gray = cv2.cvtColor(berry_image, cv2.COLOR_BGR2GRAY)

    # blurs the image so that you can get cleaner points to work with.
    berry_image_blurred = cv2.GaussianBlur(berry_image, (7, 7), 0)
    berry_image_hsv = cv2.cvtColor(berry_image_blurred, cv2.COLOR_BGR2HSV)

    # parameters for the mask, filter out black objects from white objects to detect the berries.
    # simple way to do this against a black background.
    def hsv_color_params(color):
        lower_hue = []
        upper_hue = []
        if color == 'black':
            lower_hue = np.array([0, 0, 20])
            upper_hue = np.array([255, 100, 88])
        elif color == 'white':
            lower_hue = np.array([0, 0, 0])
            upper_hue = np.array([0, 0, 255])
        return lower_hue, upper_hue

    # Compare the two images that are loded in looking for differences.
    # Main difference should be the light that turns on for each berry.
    # Function needs way more done to it.
    def compare(image1, image2):
        original = image1
        light = image2

        difference_between_images = cv2.subtract(image1, image2, )
        return difference_between_images

    chosen_color = 'black'
    lower_hue, upper_hue = hsv_color_params(chosen_color)

    black_mask = cv2.inRange(berry_image_hsv, lower_hue, upper_hue)

    berries_thresh_erode = cv2.erode(black_mask, None, iterations=3)

    berries_thresh_dilate = cv2.dilate(berries_thresh_erode, None, iterations=15)

    _, contours, hierarchy = cv2.findContours(berries_thresh_dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    berry_id = 0
    #contour_list = []
    center_of_each_berry = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 5000 and area < 32000:
            berry_id = berry_id + 1
            contour_list.append(contour)
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            print("X = ",cX)
            print("Y = ",cY)


            #cv2.putText(berry_image, "Berry {}".format(berry_id), (cX, cY - 0), cv2.FONT_HERSHEY_PLAIN, 1,
                        #(255, 255, 255), 2)

    print(berry_id, " berries detected in image!")

    # bright spot for looking for a green led in the image, will catch reflections.
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(berry_image_gray)
    cv2.circle(berry_image, maxLoc, 5, (255, 0, 0), 2)

    # Rectangles are drawn over the berries to make areas click-able for a button.
    mask = np.zeros(berry_image.shape, dtype="uint8")
    berry_rectangle_list = []
    for c in contour_list:
        (x, y, w, h) = b = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x + w, y + h), (80, 0, 255), 2)
        berry_rectangle_list.append(b)

    print(berry_rectangle_list)
    berry_image = mask

    cv2.addWeighted(mask, .5, berry_image, .1, 0, berry_image_copied)
    # Function that cleans the image mask.
    mask_overlay_cleanup(berry_image_copied)
    # print(x)
    # print(y)

    print("")
    print("Berries detected!!!!\n ...")
    print("")
    print("Opening Berry GUI. . .")

    cv2.waitKey(0)


    return berry_rectangle_list

def mask_overlay_cleanup(image):
    # pull in the image that needs to have the bounding boxes cleaned up to overlay on the image.
    dirty_image = image

    # src = cv2.imread(file_name, 1)
    temp = cv2.cvtColor(dirty_image, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(temp, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(dirty_image)
    rgba = [b, g, r, alpha]
    dst = cv2.merge(rgba, 1)
    cv2.imwrite("cleaned_berry_boxes.png", dst)