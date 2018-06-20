from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import typing
from enum import Enum


class TextWindow(QTextEdit):
    underlying_object_exists = False

    class InputMode(Enum):
        lookingForInputDevice = 0
        lookingForOutputDevice= 1
        neutral= 2

    mode = InputMode.neutral

    def __init__(self):
        super().__init__()
        self.underlying_object_exists = True
        self.setAttribute(Qt.WA_DeleteOnClose)
        doc = self.document()
        font = doc.defaultFont()
        font.setFamily('Courier New')
        doc.setDefaultFont(font)
        self.filename = None

    def contextMenuEvent(self, e: QContextMenuEvent):
        print ('context menu event! at '+  e.globalPos().__str__())
        context_menu = self.createStandardContextMenu()
        pickOutputDevice = QAction(QIcon(""), "pick an output", self)
        pickOutputDevice.triggered.connect(self.pickOutputBerry)
        context_menu.addAction(pickOutputDevice)
        context_menu.exec(e.globalPos())

    def pickOutputBerry (self):
        self.mode = self.InputMode.lookingForOutputDevice
        print ('mode is now ' + self.mode.name)

    def anOutputWasSelected(self,berryName):
        print ('reset mode to neutral, added selected berry at cursor point')
        self.mode = self.InputMode.neutral
        self.insertPlainText(berryName + '.')
        self.activateWindow()

    def getMode (self):
        return self.mode

    def closeEvent(self, event):
        # do stuff
        self.underlying_object_exists = False
        print ('reset underlying objects')
        self.save_file()
        print ('saved code')
        event.accept()  # let the window close

    def check_underlying_object (self):
        if self.underlying_object_exists == False:
            print ('init super')
            super().__init__()
            print ('super init done')
            self.underlying_object_exists = True


    def load_file(self, filename):
        self.filename = filename
        with open(filename, 'r') as f:
            s = f.read()
            self.setText(s)

    def save_file(self):
        print ('saving a file ' + self.filename)
        print ('   contents:')
        print (self.toPlainText())
        with open(self.filename, 'w') as f:
            f.write(self.toPlainText())


class PictureWindow(QGraphicsView):
    def __init__(self, picture, click_signal):
        self.scene = QGraphicsScene()
        self.picture = PictureObject(picture)
        self.scene.addItem(self.picture)
        self.scene.setSceneRect(0, 0, self.picture.width(), self.picture.height())
        super().__init__(self.scene)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.clickable_berries = {}
        self.click_signal = click_signal

    def fit_window(self):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def set_picture(self, img):
        self.scene.removeItem(self.picture)
        self.picture = PictureObject(img)
        self.scene.addItem(self.picture)
        self.scene.setSceneRect(0, 0, self.picture.width(), self.picture.height())

    def show_berries(self, berry_map: dict):
        for overlay in self.clickable_berries.values():
            self.scene.removeItem(overlay)
        self.clickable_berries.clear()
        for berry_name in berry_map.keys():
            pos = berry_map[berry_name]
            overlay = BerryOverlay(pos, berry_name, self.click_signal)
            self.clickable_berries[berry_name] = overlay
            self.scene.addItem(overlay)


class PictureObject(QGraphicsItem):
    def __init__(self, picture):
        super().__init__()
        if type(picture) is str:
            self.pixmap = QPixmap(picture)
        else:
            height, width, channel = picture.shape
            self.pixmap = QPixmap(QImage(picture.data, width, height, 3 * width, QImage.Format_RGB888))

    def boundingRect(self):
        return QRectF(0, 0, self.pixmap.width(), self.pixmap.height())

    def paint(self, painter: QPainter, option, widget: typing.Optional[QWidget] = ...):
        painter.drawPixmap(0, 0, self.pixmap)
        painter.setPen(QColor(255, 0, 0, 127))
        painter.drawRect(self.boundingRect())

    def height(self):
        return self.pixmap.height()

    def width(self):
        return self.pixmap.width()


class BerryOverlay(QGraphicsObject):
    def __init__(self, pos, name, signal):
        super().__init__()
        x = pos[0]
        y = pos[1]
        self.pos = pos
        self.overlay = QRectF(x - 30, y - 30, 60, 60)
        self.name = name
        self.click_signal = signal

    def boundingRect(self):
        return self.overlay

    def shape(self):
        x = self.pos[0]
        y = self.pos[1]
        path = QPainterPath()
        path.addEllipse(x - 30, y - 30, 60, 60)
        return path

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...):
        painter.setPen(QColor(255, 0, 0, 127))
        painter.drawPath(self.shape())

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):
        print('Clicked berry!')
        self.click_signal.emit(self.name)
