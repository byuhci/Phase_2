import cv2
from skimage.measure import compare.ssim
import imutils
import numpy as np

image1 = cv2.imread("berry_without_light.jpg")
image2 = cv2.imread("berry_with_light.jpg")


grayed_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
grayed_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

(score,diff) = compare_ssim(grayed_image1, grayed_image2, full=True)





cv2.imwrite("differece_between_images.jpg", difference_between_images)
