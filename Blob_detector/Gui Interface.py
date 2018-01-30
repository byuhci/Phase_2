import sys
from PyQt5,QtWidgets import QApplication,Qwidget

app = QtGui.QApplication(sys.argv)

window = QtGui.QWidget()
window = setGeometry(50,50,500,300)
window.setWindowTitle("PyQt Gui!")

window.show()