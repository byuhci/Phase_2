from PyQt5 import QtCore
from PyQt5 import QtGui


class QLabelButton(QtGui.QLabel):

    def __init(self, parent):
        QtGui.QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))

class CustomButton(QtGui.QWidget):
    def __init__(self, parent=None, *args):
        super(CustomButton, self).__init__(parent)
        self.setMinimumSize(300, 350)
        self.setMaximumSize(300, 350)

        pixmap = QtGui.QPixmap('D:\mario.png')

        self.button = QLabelButton(self)
        self.button.setPixmap(pixmap)
        self.button.setScaledContents(True)
        self.button.setMask(pixmap.mask()) # THIS DOES THE MAGIC

        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.onClick)

    def onClick(self):
        print('Button was clicked')