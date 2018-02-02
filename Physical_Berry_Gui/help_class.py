import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import text_editor_class
from cv2 import *


class Ui_Help(object):
    def setupUi(self, Help):
        Help.setObjectName("Help")
        Help.resize(251, 99)
        icon = QIcon()
        icon.addPixmap(QPixmap("logo.png"), QIcon.Normal, QIcon.Off)
        Help.setWindowIcon(icon)
        self.gridLayoutWidget = QWidget(Help)
        self.gridLayoutWidget.setGeometry(QRect(9, 9, 231, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEdit = QPlainTextEdit(self.gridLayoutWidget)
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setFrameShape(QFrame.WinPanel)
        self.plainTextEdit.setFrameShadow(QFrame.Sunken)
        self.plainTextEdit.setLineWidth(1)
        self.plainTextEdit.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 1)

        self.retranslateUi(Help)
        QMetaObject.connectSlotsByName(Help)