
## Gui Element for the link between worlds project:
"""
     *****************************
     Written by casey walker
     *****************************
     all elements in the gui are contained here.
     functions for the berry stuff are handled on the berry network side but are called here.

"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import text_editor_class
import cv2
from python_src import *
from python_src.berry_api import *
from python_src.berry_factory import berry_factory
import sys
from time import sleep
import MainGui
from detect_berries_in_image import berry_detection
import numpy as np
# from light_seeker import light_seeker
import random



class Window(QMainWindow):

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
        self.setGeometry(100,200,1280,775)
        self.statusBar()
        extract_action = QAction("Save & Exit",self)
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
        #fileMenu = mainMenu.addMenu("&Help")
        #fileMenu.addAction(help)

        self.setWindowIcon(QIcon(icons_path+"berry_icon.png"))
        #self.home_window()

        # Toolbars initialized here
        # toolbar menu icon set here
        # Triggering actions are assigned here

        extract_action_toolbar_berry = QAction(QIcon(icons_path+"flatberry.png"), "Connect to the berriez", self)
        extract_action_toolbar_berry.triggered.connect(self.close)

        self.toolBar = self.addToolBar("BeRRY")
        self.toolBar.addAction(extract_action_toolbar_berry)

        extract_action_toolbar_berry = QAction(QIcon(icons_path+"camera.png"), "Take Picture Using Webcamz", self)
        extract_action_toolbar_berry.triggered.connect(self.camera)

        self.toolBar = self.addToolBar("Camera toolbar")
        self.toolBar.addAction(extract_action_toolbar_berry)

        extract_action_toolbar_berry = QAction(QIcon(icons_path+"lights.png"), "Flashes the lightz", self)
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
        #self.mouse_position_tracker(self)

        self.show()

    def help_window(self):
        self.newWindow.show()

    def quit(self):
        print("Quiting out, Thanks...")
        choice = QMessageBox.question(self, "Close Application", "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Quiting Berry GUI")
            sys.exit()
        else:
            pass

    def editor(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

    def look_for_files(self):
        print("Looking for all of your files...")

    def file_Open(self):

        name, _ = QFileDialog.getOpenFileName(self, "Open File")

        print(name)


        self.editor()
        with open(name, "r") as file:
            text = file.read()
            self.textEdit.setText(text)

    def editor_window(self):
        text_editor_class.main()
        print("Showing the Editor")

    def camera(self):
        # initialize the camera

        # self.berry_detection_bounding_box = berry_detection()


        cam = cv2.VideoCapture(0)  # 0 -> index of camera
        s, img = cam.read()

        if s:  # frame captured without any errors
            #namedWindow("Berry Snapper")
            img = cv2.resize(img, None, fx=2, fy=1.5)
            cv2.imshow("Berry Snapper", img)
            #img = cv2.resize(img, None, 2,2, interpolation=cv2.INTER_AREA)
            cv2.waitKey(0)
            cv2.destroyWindow("Berry Snapper")
            cv2.imwrite("CRAZY.jpg", img)  # save image
            self.berry_image = img
            self.berry_detection_bounding_box = berry_detection()

            cv2.waitKey()

    def generate_files_to_be_edited(self):
        # files for all the berry types in the project are to be generated here.
        global berry_detection_bounding_box
        if berry_detection_bounding_box > 0:
            # check to see if there are any bounding boxes.
            berry_detection()
        return None



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
        #pixmap = QPixmap('cleaned_berry_boxes.png')
        label.setPixmap(pixmap)

        label.resize(pixmap.width(), pixmap.height())
        label.move(0, self.OFFSET_FOR_THE_IMAGE)

        self.layout.addWidget(label)

        label.resize(pixmap.width(), pixmap.height())
        label.move(0, self.OFFSET_FOR_THE_IMAGE)

        self.layout.addWidget(label)
        self.show()


    def on_pushButton_click(self):
            self.newWindow.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"sample_code_stub.txt")
        self.show()
        ## fileName = self.file_Open()
        self.newWindow.show()
        #openFile.triggered.connect(self.file_Open)
        if fileName:
            print(fileName)
            #self.file_Open

    def mousePressEvent(self, QMouseEvent):

        # I need to get the list here to get the click-able areas,but it is proving difficult.
        click_x = QMouseEvent.pos().x()
        click_y = QMouseEvent.pos().y() - self.OFFSET_FOR_THE_IMAGE
        print(click_x,click_y)
        if self.berry_detection_bounding_box is None:
            print("no berries baby")
            return

        for x, y, w, h in self.berry_detection_bounding_box:
            # thank kristian for this nonsense
            if (click_x - x) * (click_x - (x+w)) <= 0 and (click_y - y) * (click_y - (y+h)) <= 0:
                print("click inside of the berry box")
                self.newWindow.show()
        print("Done")

    #berry_image = np.zeroes(self.berry_image.shape, dtype="uibt8")


    def light_sequence(self):
        # This function will run through the lights identifying the berries.
        berry_list = []
        init_host(sys.argv)

        berry_list = get_berry_list()
        berries = [berry_factory('Name Your Berry', berry[0], berry[1]) for berry in berry_list]

        btn = None
        led = None
        slider = None
        knob = None

        for berry in berries:
            print('name: {}, type: {}, guid: {}'.format(berry.name, berry.berry_type, berry.addr))

        #print("did you get here??") Worked
        for berry in berries:
            #led.color = [0,0,0]
            print(berry.berry_type)
            print("next berry : \n")
            berry.set_status_led(1)
            #image_difference = light_seeker()
            #image_difference
            sleep(2)
            berry.set_status_led(0)
            #berry_detection()
            # this is all working, th light seekere image processing is the main crux in the loop.
        #
        # # loops forever, make it walk through the sequence once getting all of the berries.
        # try:
        #     v = 0
        #     i = 0
        #     while berry_list<len(berries):
        #         berries[i].set_status_led(v)
        #         i = (i + 1) % len(berries)
        #         v = berry_list.randint(0, 1)
        #         if btn.state == 1:
        #             led.color = [150, 150, 150]
        #         else:
        #             led.color = [0, 0, 0]
        #         sleep(1)
        # """
        # except:
        #     print('End')



class help(QMainWindow):
    def __init__(self, parent=None):
        super(help, self).__init__(parent)
        #init_host(argv)
        berry_list = get_berry_list()
        print(berry_list)
        self.statusBar()
        extract_action = QAction("Save & Exit", self)
        extract_action.setShortcut("Ctrl+q")
        extract_action.setStatusTip("Leave the app")
        extract_action.triggered.connect(self.quit)

        extract_action_edit = QAction("Show files", self)
        extract_action_edit.setShortcut("Ctrl+f")
        extract_action_edit.setStatusTip("Looking for files")
        extract_action_edit.triggered.connect(self.quit)


        openFile = QAction("Open File", self)
        openFile.setShortcut("Ctrl+o")
        openFile.setStatusTip("Open File")
        openFile.triggered.connect(self.file_Open)


        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(extract_action)
        fileMenu.addAction(openFile)

        # Setting a title, locating and sizing the window
        self.title = 'Text Editor'
        self.left = 200
        self.top = 200
        self.width = 500
        self.height = 700
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.textEdit = QTextEdit()


        self.setCentralWidget(self.textEdit)

        self.pushButton = QPushButton("Close Me", self)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pushButton.move(400,600)
        self.pushButton.setVisible(True)


    def main(self,argv):
        init_host(argv)
        berry_list = get_berry_list()
        berries = [berry_factory('yo', berry[0], berry[1]) for berry in berry_list]

        btn = None
        led = None
        for berry in berries:
            print('name: {}, type: {}, guid: {}'.format(berry.name, berry.berry_type, berry.addr))
            if berry.berry_type == 'Button':
                btn = berry
            if berry.berry_type == 'RGB':
                led = berry

        try:
            v = 0
            i = 0
            while True:
                berries[i].set_status_led(v)
                i = (i + 1) % len(berries)
                v = random.randint(0, 1)
                if btn.state == 1:
                    led.color = [150, 150, 150]
                else:
                    led.color = [0, 0, 0]
                sleep(.01)
        except:
            print('End')

    def on_pushButton_clicked(self):
        self.close()

    def quit(self):
        print("Quiting out, Thanks...")
        choice = QMessageBox.question(self, "Close Application", "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Quiting Berry GUI")
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
"""
class code_editor(QMainWindow):
    def __init__(self, parent=None):
        super(code_editor, self).__init__(parent)
        self.statusBar()
        extract_action = QAction("Save & Exit", self)
        extract_action.setShortcut("Ctrl+q")
        extract_action.setStatusTip("Leave the app")
        extract_action.triggered.connect(self.quit)

        extract_action_edit = QAction("Show files", self)
        extract_action_edit.setShortcut("Ctrl+f")
        extract_action_edit.setStatusTip("Looking for files")
        extract_action_edit.triggered.connect(self.quit)


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

        # Setting a title, locating and sizing the window
        self.title = 'Code Editor'
        self.left = 200
        self.top = 200
        self.width = 500
        self.height = 900
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.textEdit = QTextEdit()

        self.setCentralWidget(self.textEdit)

        self.pushButton = QPushButton("Close Me", self)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pushButton.move(400,800)
        self.pushButton.setVisible(True)

    def on_pushButton_clicked(self):
        self.close()

    def quit(self):
        print("Quiting out, Thanks...")
        choice = QMessageBox.question(self, "Close Application", "Are you sure you want to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Quiting Berry GUI")
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
"""


def main():
    app = QApplication(sys.argv)
    gui = Window()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

