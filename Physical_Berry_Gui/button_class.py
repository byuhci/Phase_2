



import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QLabelButton(QLabel):

    def __init(self, parent):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))

class CustomButton(QtGui.QWidget):
    def __init__(self, parent=None, *args):
        super(CustomButton, self).__init__(parent)
        self.setMinimumSize(300, 350)
        self.setMaximumSize(300, 350)
        #
        # This needs to be altered to a specific region on the image and not a jpg
        pixmap = QPixmap('detected_berries.jpg')

        self.button = QLabelButton(self)
        self.button.setPixmap(pixmap)
        self.button.setScaledContents(True)
        self.button.setMask(pixmap.mask()) # THIS DOES THE MAGIC

        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.onClick)

    def onClick(self):
        print('Button was clicked')


