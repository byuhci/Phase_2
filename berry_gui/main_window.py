import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    OFFSET_FOR_THE_IMAGE = 55

    def __init__(self):
        super().__init__()
        self.berry_detection_bounding_box = None
        self.berry_image = None
        self.berry_image_difference = None
        self.init_ui()
        self.background = "background.jpg"

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
        openEditor.triggered.connect(self.editor)

        openFile = QAction("Open File", self)
        openFile.setShortcut("Ctrl+o")
        openFile.setStatusTip("Open File")
        openFile.triggered.connect(self.file_Open)

        self.pushButton = QPushButton("New Window", self)
        self.pushButton.move(120, 120)
        self.pushButton.clicked.connect(self.help_window)
        self.newWindow = help(self)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(extract_action)
        fileMenu.addAction(openFile)
        fileMenu = mainMenu.addMenu("&Editor")
        fileMenu.addAction(openEditor)
        # fileMenu = mainMenu.addMenu("&Help")
        # fileMenu.addAction(help)

        self.setWindowIcon(QIcon(icons_path + "berry_icon.png"))
        # self.home_window()

        # Toolbars initialized here
        # toolbar menu icon set here
        # Triggering actions are assigned here


        extract_action_toolbar_berry = QAction(QIcon(icons_path + "flatberry.png"), "Connect to the berries", self)
        extract_action_toolbar_berry.triggered.connect(self.close)

        self.toolBar = self.addToolBar("BeRRY")
        self.toolBar.addAction(extract_action_toolbar_berry)

        extract_action_toolbar_berry = QAction(QIcon(icons_path + "camera.png"), "Take Picture Using Webcam", self)
        extract_action_toolbar_berry.triggered.connect(self.camera)

        self.toolBar = self.addToolBar("Camera toolbar")
        self.toolBar.addAction(extract_action_toolbar_berry)

        extract_action_toolbar_berry = QAction(QIcon(icons_path + "lights.png"), "Flashes the lights", self)
        extract_action_toolbar_berry.triggered.connect(self.light_sequence)

        self.toolBar = self.addToolBar("Lights toolbar")
        self.toolBar.addAction(extract_action_toolbar_berry)

        extract_action_toolbar_berry = QAction(QIcon(""), "Opens the Editor", self)
        extract_action_toolbar_berry.triggered.connect(self.editor_window)

        self.toolBar = self.addToolBar("Editor")
        self.toolBar.addAction(extract_action_toolbar_berry)

        extract_action_toolbar_berry = QAction(QIcon(""), "Set the image", self)
        extract_action_toolbar_berry.triggered.connect(self.reset_background)

        self.toolBar = self.addToolBar("Reset Background")
        self.toolBar.addAction(extract_action_toolbar_berry)

        self.layout = QGridLayout()

        self.reset_background()

        self.setMouseTracking(True)
        self.mousePressEvent(self)
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
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

    def editor_window(self):
        text_editor_class.main()
        print("Showing the Editor")

    def camera(self):
        # initialize the camera

        # self.berry_detection_bounding_box = berry_detection()

        cam = cv2.VideoCapture(0)  # 0 -> index of camera
        s, img = cam.read()

        if s:  # frame captured without any errors
            # namedWindow("Berry Snapper")
            img = cv2.resize(img, None, fx=2, fy=1.5)
            cv2.imshow("Berry Snapper", img)
            # img = cv2.resize(img, None, 2,2, interpolation=cv2.INTER_AREA)
            cv2.waitKey(0)
            cv2.destroyWindow("Berry Snapper")
            cv2.imwrite("CRAZY.jpg", img)  # save image
            self.berry_image = img
            self.berry_detection_bounding_box = berry_detection()

            cv2.waitKey()
