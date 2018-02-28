import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def mousePressEvent(self, QMouseEvent):
        print(QMouseEvent.pos())

    def mouseReleaseEvent(self, QMouseEvent):
        cursor = QCursor()
        print(cursor.pos())

    def initUI(self):
        qbtn = QPushButton('Quit', self)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)

        #self.setGeometry(100, 100, 1024, 768)
        #self.setWindowTitle('Quit button')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.show()
    def test(self):
      print("test")

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
