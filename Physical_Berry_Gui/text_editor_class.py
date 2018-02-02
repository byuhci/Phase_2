import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
"""
class Berry_Editor(QWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    #def sizeHint(self):
        #return self.ui

    def init_ui(self):
        self.setWindowTitle("Berry Editor")
        self.setGeometry(100, 200, 600, 900)

        self.setWindowIcon(QIcon("berry_icon.png"))

        extract_action = QAction("Save & Exit",self)
        extract_action.setShortcut("Ctrl+Q")
        extract_action.setStatusTip("Leave the app")
        extract_action.triggered.connect(self.quit)

        extract_action_edit = QAction("Show files", self)
        extract_action_edit.setShortcut("Ctrl+f")
        extract_action_edit.setStatusTip("Looking for files")
        extract_action_edit.triggered.connect(self.quit)


        openEditor = QAction("Editor", self)
        openEditor.setShortcut("Ctrl+E")
        openEditor.setStatusTip("Open Editor")
        openEditor.triggered.connect(self.editor)

        openFile = QAction("Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip("Open File")
        openFile.triggered.connect(self.file_Open)
        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(extract_action)
        fileMenu.addAction(openFile)
        fileMenu = mainMenu.addMenu("&Editor")
        fileMenu.addAction(openEditor)


        self.show()


    def quit(self):
        print("Quiting out, Thanks...")
        choice = QMessageBox.question(self, "Close Application", "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Quiting Berry Editor")
            sys.exit()
        else:
            pass

    def file_Open(self):
        name, _ = QFileDialog.getOpenFileName(self, "Open File")

        print(name)


        self.editor()
        with open(name, "r") as file:
            text = file.read()
            self.textEdit.setText(text)

    def editor(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

"""


class Editor_window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'BERRY CODE EDITOR'


        self.left = 200
        self.top = 200
        self.width = 640
        self.height = 980

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon("berry_icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.editor()

        #self.statusBar()

        extract_action = QAction("Save & Exit", self)
        extract_action.setShortcut("Ctrl+Q")
        extract_action.setStatusTip("Leave the app")
        extract_action.triggered.connect(self.quit)

        extract_action_edit = QAction("Show files", self)
        extract_action_edit.setShortcut("Ctrl+f")
        extract_action_edit.setStatusTip("Looking for files")
        extract_action_edit.triggered.connect(self.quit)

        openEditor = QAction("Editor", self)
        openEditor.setShortcut("Ctrl+E")
        openEditor.setStatusTip("Open Editor")
        openEditor.triggered.connect(self.editor)

        openFile = QAction("Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip("Open File")
        openFile.triggered.connect(self.file_Open)


        """
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(extract_action)
        fileMenu.addAction(openFile)
        fileMenu = mainMenu.addMenu("&Editor")
        fileMenu.addAction(openEditor)
        """
        #self.textEdit = QTextEdit()
        #self.QWidget(self.textEdit)
        self.show()


    def editor(self):
        self.text_edit = QTextEdit()
        #self.setCentralWidget(self.text_edit)


    def file_Open(self):
        name, _ = QFileDialog.getOpenFileName(self, "Open File")

        print(name)


        self.editor()
        with open(name, "r") as file:
            text = file.read()
            self.textEdit.setText(text)

    def quit(self):
        print("Quiting out, Thanks...")
        choice = QMessageBox.question(self, "Close Application", "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Quiting Berry GUI")
            sys.exit()
        else:
            pass



def main():
    app = QApplication(sys.argv)
    gui = Editor_window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
