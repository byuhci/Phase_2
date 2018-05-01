from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class TextWindow(QTextEdit):

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

    def load_file(self, filename):
        with open(filename, 'r') as f:
            s = f.read()
            self.setText(s)


class PictureWindow(QLabel):

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

    def set_picture(self, picture):
        pxm = QPixmap(picture)
        self.setPixmap(pxm)
        self.show()

