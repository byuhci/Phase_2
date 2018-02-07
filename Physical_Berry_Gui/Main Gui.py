import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import cv2
import window_class



def main():

    def berry_detection():

        berry_image = cv2.imread("berry_picture.jpg")

        berry_image_copied = berry_image.copy()

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
        contour_list = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 5000 and area < 32000:
                berry_id = berry_id + 1
                contour_list.append(contour)
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                cv2.putText(berry_image, "Berry {}".format(berry_id), (cX, cY - 80), cv2.FONT_HERSHEY_PLAIN, 1,
                            (255, 255, 255), 2)


        print(berry_id, " berries detected in image!")

        # bright spot for looking for a green led in the image, will catch reflections.
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(berry_image_gray)
        cv2.circle(berry_image, maxLoc, 5, (255, 0, 0), 2)
        #cv2.imshow("", berry_image)

        # Rectangles are drawn over the berries to make areas click-able for a button.
        mask = np.zeros(berry_image.shape, dtype="uint8")

        for c in contour_list:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 0), 3)
        berry_image_copied = mask

        cv2.addWeighted(mask, .5, berry_image_copied, .1, 0, berry_image_copied)



        # cv2.drawContours(berry_image,contour_list, -1,(0,255,0),2)
        # show the points that are detected
        cv2.imshow("Detected Berries", berry_image_copied)
        cv2.imwrite("detected_berries.jpg", berry_image_copied)
        print(mask)

        print("")
        print("Berries detected!!!!\n ...")
        print("")
        print("Opening Berry GUI. . .")


        cv2.waitKey(0)



    berry_detection()


    window_class.main()

    ######text_editor_class.main()
    #Image_loaded_from_camera

    ## Inside of th load the image function run all of the image processing.

    ## Run the Gui and import the processed image.

    ## Have the Button class here for the button click events on the berry.

    ## Text editor window class that imports code stub
        ## import the code stub from the berry basket.

    ## Save out the files into one directory

    ## Compile all the code stubs into a single file to run.

    ## After all programming is done have a Run function or a save command


if __name__ == '__main__':
    main()




