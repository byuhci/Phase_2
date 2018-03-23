import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
from cv2 import *
from python_src import *
from python_src.berry_api import *
from detect_berries_in_image import berry_detection
from python_src.berry_factory import berry_factory
import sys
from time import sleep
import random
import window_class



contour_list = []

def main():

    # berry list. Has all of the values like Guid and type.
    #berry_list = get_berry_list()

    #berry_detection()

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




