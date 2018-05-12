from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import typing


class TextWindow(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

    def load_file(self, filename):
        with open(filename, 'r') as f:
            s = f.read()
            self.setText(s)


class PictureWindow(QGraphicsView):
    def __init__(self, picture):
        self.scene = QGraphicsScene()
        self.picture = PictureObject(picture)
        self.scene.addItem(self.picture)
        self.scene.setSceneRect(0, 0, self.picture.width(), self.picture.height())
        super().__init__(self.scene)
        self.setAttribute(Qt.WA_DeleteOnClose)


class PictureObject(QGraphicsItem):
    def __init__(self, picture):
        super().__init__()
        self.pixmap = QPixmap(picture)

    def boundingRect(self):
        return QRectF(-50, -50, 100, 100)

    def paint(self, painter: QPainter, option, widget: typing.Optional[QWidget] = ...):
        painter.drawPixmap(0, 0, self.pixmap)
        painter.setPen(QColor(255, 0, 0, 127))
        painter.drawRect(self.boundingRect())

    def height(self):
        return self.pixmap.height()

    def width(self):
        return self.pixmap.width()


class BerryOverlay(QGraphicsItem):
    def __init__(self, rect: QRectF):
        super().__init__()
        self.overlay = rect

    def boundingRect(self):
        return self.overlay

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...):
        painter.setPen(QColor(255, 0, 0, 127))
        painter.drawRect(self.boundingRect())
