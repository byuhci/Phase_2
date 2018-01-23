import argparse
import cv2

# global variables that will be used for the crop region and cropping operator
reference_point = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    # grab a reference to the global variables so they can be used.
    global reference_point, cropping
    # if th left mouse button was clicked the record it as the start
    #(x,y) are to show that the cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        reference_point = [(x,y)]
        cropping = True

    # end of the clicking event, add the crop location to the list.
    elif event == cv2.EVENT_LBUTTONUP:
        reference_point.append((x,y))
        cropping = False

    #draw a rectangle to indicate the cropped region
        cv2.rectangle(image, reference_point[0], reference_point[1], (0,255,0), 2)
        cv2.imshow("image", image)


# create an argument parser and then parse all of the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(parser.parse_args())
print(args)
# parses through the image copies it and sets it to a new window.
image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("CROP")
cv2.setMouseCallback("CROPPED", click_and_crop)


# loops through looking for string inputs to know if to reset or to crop.
while True:
    # display the window and show when a button is pressed
    cv2.imshow("image", image)
    key = cv2.waitKey(1) &0xFF

    if key == ord("r"):
        image = clone.copy()

    elif key == ord("c"):
        break

#creats a new window with the cropped region and display it, can handle up to two regions of interest.
if len(reference_point) == 2:
    roi = clone[reference_point[0][1]: reference_point[1][1], reference_point[0][0]:reference_point[1][0]]
    cv2.imshow("ROI", roi)
    cv2.waitKey(0)

cv2.destroyAllWindows()



