import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subwindow import *
from project_manager import ProjectManager


class MainWindow(QMainWindow):
    OFFSET_FOR_THE_IMAGE = 55

    def __init__(self):
        super().__init__()
        self.berry_detection_bounding_box = None
        self.berry_image = 'berry_picture.jpg'
        self.berry_image_difference = None
        self.mdiArea = QMdiArea()
        self.background = "background.jpg"
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.init_ui()

    def init_ui(self):
        icons_path = "icons/"

        self.setWindowTitle("Berry GUI")
        self.setGeometry(100, 200, 1280, 775)
        self.statusBar()
        extract_action = QAction("Save & Exit", self)
        extract_action.setShortcut("Ctrl+q")
        extract_action.setStatusTip("Leave the app")
        extract_action.triggered.connect(self.quit)

        extract_action_edit = QAction("Show files", self)
        extract_action_edit.setShortcut("Ctrl+f")
        extract_action_edit.setStatusTip("Looking for files")
        extract_action_edit.triggered.connect(self.quit)

        openEditor = QAction("Editor", self)
        openEditor.setShortcut("Ctrl+E")
        openEditor.setStatusTip("Open Editor")
        openEditor.triggered.connect(self.open_editor)

        openFile = QAction("Open File", self)
        openFile.setShortcut("Ctrl+o")
        openFile.setStatusTip("Open File")
        # openFile.triggered.connect(self.file_Open)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(extract_action)
        fileMenu.addAction(openFile)
        fileMenu = mainMenu.addMenu("&Editor")
        fileMenu.addAction(openEditor)
        # fileMenu = mainMenu.addMenu("&Help")
        # fileMenu.addAction(help)

        self.setWindowIcon(QIcon(icons_path + "berry_icon.png"))

        extract_action_toolbar_berry = QAction(QIcon(icons_path + "flatberry.png"), "Connect to the berries", self)
        extract_action_toolbar_berry.triggered.connect(self.open_project)

        self.toolBar = self.addToolBar("BeRRY")
        self.toolBar.addAction(extract_action_toolbar_berry)

        extract_action_toolbar_berry = QAction(QIcon(icons_path + "camera.png"), "Take Picture Using Webcam", self)
        extract_action_toolbar_berry.triggered.connect(self.show_picture)

        self.toolBar = self.addToolBar("Camera toolbar")
        self.toolBar.addAction(extract_action_toolbar_berry)

        extract_action_toolbar_berry = QAction(QIcon(icons_path + "lights.png"), "Flashes the lights", self)
        # extract_action_toolbar_berry.triggered.connect(self.light_sequence)

        self.toolBar = self.addToolBar("Lights toolbar")
        self.toolBar.addAction(extract_action_toolbar_berry)

        extract_action_toolbar_berry = QAction(QIcon(""), "Opens the Editor", self)
        extract_action_toolbar_berry.triggered.connect(self.open_editor)

        self.toolBar = self.addToolBar("Editor")
        self.toolBar.addAction(extract_action_toolbar_berry)

        extract_action_toolbar_berry = QAction(QIcon(""), "Set the image", self)
        # extract_action_toolbar_berry.triggered.connect(self.reset_background)

        self.toolBar = self.addToolBar("Reset Background")
        self.toolBar.addAction(extract_action_toolbar_berry)

        # self.layout = QGridLayout()
        # self.reset_background()

        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        bg = QPixmap(self.background)
        bg.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        self.mdiArea.setBackground(QBrush(bg))
        self.mdiArea.setOption(QMdiArea.DontMaximizeSubWindowOnActivation)
        self.setCentralWidget(self.mdiArea)

        # self.setMouseTracking(True)
        # self.mousePressEvent(self)
        # self.mouse_position_tracker(self)

        self.show()

    def help_window(self):
        self.newWindow.show()

    def quit_window(self):
        print("Quiting out, Thanks...")
        choice = QMessageBox.question(self, "Close Application", "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Quiting Berry GUI")
            sys.exit()
        else:
            pass

    def open_editor(self):
        child = TextWindow()
        sw = self.mdiArea.addSubWindow(child)
        sw.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        child.show()

    def show_picture(self):
        child = PictureWindow(self.berry_image)
        sw = self.mdiArea.addSubWindow(child)
        # sw.setWindowFlags()
        sw.showMaximized()
        child.show()
        self.threadpool.start(Worker(self.manager.find_berries))

    def quit(self):
        print("Quiting out, Thanks...")
        choice = QMessageBox.question(self, "Close Application", "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Quiting Berry GUI")
            sys.exit()
        else:
            pass

            # This function pulls in the initial berry picture and iw will set it as the background of the Gui.

    def reset_background(self):

        label = QLabel(self)
        pixmap = QPixmap('background.jpg')
        label.setPixmap(pixmap)

        label.resize(pixmap.width(), pixmap.height())
        label.move(0, self.OFFSET_FOR_THE_IMAGE)

        self.layout.addWidget(label)

        label.resize(pixmap.width(), pixmap.height())
        label.move(0, self.OFFSET_FOR_THE_IMAGE)

        self.layout.addWidget(label)

        label = QLabel(self)
        # pixmap = QPixmap('cleaned_berry_boxes.png')
        label.setPixmap(pixmap)

        label.resize(pixmap.width(), pixmap.height())
        label.move(0, self.OFFSET_FOR_THE_IMAGE)

        self.layout.addWidget(label)

        self.show()

    def open_project(self):
        dialog = QFileDialog()
        filepath = dialog.getExistingDirectory(self, 'Choose existing project or create a new folder', './')
        self.manager = ProjectManager(filepath)
        self.manager.sync_project()


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)


def main():
    app = QApplication(sys.argv)
    gui = MainWindow()
    sys.exit(app.exec_())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    main()
