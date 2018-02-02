from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class CustomButton(QWidget):

    def __init__(self, parent, image):
        super(CustomButton, self).__init__(parent)
        self.image = image

    def sizeHint(self):
        return self.image.size()

    def mouseReleaseEvent(self, event):
        # Position of click within the button
        pos = event.pos()
        # Assuming button is the same exact size as image
        # get the pixel value of the click point.
        pixel = self.image.alphaChannel().pixel(pos)

        if pixel:
            # Good click, pass the event along, will trigger a clicked signal
            super(CustomButton, self).mouseReleaseEvent(event)
        else:
            # Bad click, ignore the event, no click signal
            event.ignore()

def main():
    CustomButton

main()