import numpy as np
import matplotlib
import opencv
import cv2.aruco
import cv2
import json



#use the on board video camera to get image.
video_capture = cv2.VideoCapture()


#make an empty list assuming the Json is a list of IDs.
list_for_importing_berries = {}
# puts the Json list into a python list so was can assign image recognizers.
list_of_berries = json.loads(list_for_importing_berries)

##############
# Run image processing, blob detection looking for the shapes of th berries.
##############

##############
# Now look for the light led to identify the berry that is indicated.
##############


##############
# Draw an area around the berry that is annotated with its name.
##############

##############
# make the region clickable
##############

##############
# Tie the click to a text editor that pulls up the code stubs from the berry IDE
##############

##############
# Export all the edited code to a file (something like notepad)
##############