import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subwindow import *
from project_manager import ProjectManager
from python_src.berry import Berry

class MainWindow(QMainWindow):
    OFFSET_FOR_THE_IMAGE = 55
    signal = pyqtSignal()
    clickSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.berry_detection_bounding_box = None
        self.berry_image = 'berry_picture.jpg'
        self.berry_image_difference = None
        self.mdiArea = QMdiArea()
        self.background = "background.jpg"
        self.threadpool = QThreadPool()
        self.signal.connect(self.finished_find)
        self.clickSignal.connect(self.clicked_berry)
        self.picture_window = None
        self.text_window = None
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.init_ui()

    def init_ui(self):
        icons_path = "icons/"

        self.setWindowTitle("Berry GUI")
        self.setGeometry(100, 200, 1280, 775)
        self.statusBar().showMessage('idle')
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

        extract_action_toolbar_berry = QAction(QIcon(icons_path + "camera.png"), "Take Picture Using Webcamz", self)
        extract_action_toolbar_berry.triggered.connect(self.show_picture)

        self.toolBar = self.addToolBar("Camera toolbar")
        self.toolBar.addAction(extract_action_toolbar_berry)

        onlyIoAction = QAction(QIcon(""),"outputs",self)
        onlyIoAction.triggered.connect(self.showOutputBerries)

        self.toolBar.addAction(onlyIoAction)

        onlyIoAction = QAction(QIcon(""),"inputs",self)
        onlyIoAction.triggered.connect(self.showInputBerries)

        self.toolBar.addAction(onlyIoAction)


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

        save_action = QAction(QIcon(icons_path + 'save.png'), 'Saves the currently open code window', self)
        save_action.triggered.connect(self.save_file)
        self.toolBar = self.addToolBar('Save code')
        self.toolBar.addAction(save_action)

        run_action = QAction(QIcon(icons_path + 'play.png'), 'Runs the project', self)
        run_action.triggered.connect(self.run_project)
        self.toolBar = self.addToolBar('Run project')
        self.toolBar.addAction(run_action)

        # self.layout = QGridLayout()
        # self.reset_background()

        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        bg = QPixmap(self.background)
        bg.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        self.mdiArea.setBackground(QBrush(bg))
        self.mdiArea.setOption(QMdiArea.DontMaximizeSubWindowOnActivation)
        self.setCentralWidget(self.mdiArea)

        self.picture_window = PictureWindow(self.background, self.clickSignal)
        self.mdiArea.addSubWindow(self.picture_window)
        self.picture_window.showMaximized()

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
        self.threadpool.start(Worker(self.manager.find_berries, self.signal))

    def showOutputBerries (self):
        self.threadpool.start(Worker(self.manager.find_berries, self.signal, Berry.BerryClasses.output))

    def showInputBerries (self):
        self.threadpool.start(Worker(self.manager.find_berries,self.signal, Berry.BerryClasses.input))

    def setupsubwindow (self):
        self.text_window = TextWindow()
        self.text_sub = self.mdiArea.addSubWindow(self.text_window)
        self.text_sub.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)

    def loadupberryfile (self, name):
        print ('load code for berry named' + name)
        filename = self.manager.pick_berry(name)
        self.text_window.load_file(filename)
        self.text_sub.setWindowTitle(name)
        self.text_window.show()

    @pyqtSlot(str)
    def clicked_berry(self, name):
        print ('someone clicked a berry named '+ name)
        if self.text_window is None:
            print ('there was no subwindow for the code')
            self.setupsubwindow()
            self.loadupberryfile(name)
            print ('... made a subwindow for code')
        else:
            print('subwindow mode is ' + self.text_window.mode.name)
            if (self.text_window.mode == self.text_window.InputMode.lookingForOutputDevice  and self.text_window.underlying_object_exists):
                print ('clicked a berry in output device mode... stick it in the code')
                self.text_window.anOutputWasSelected(name)
            else:
                # just in normal mode re make the underlying object if needed.
                # and always load up the berry code file into the subwindow.
                print ('clicked a berry, the window already exists, but we are not in select output mode')
                if (not self.text_window.underlying_object_exists):
                    self.setupsubwindow()
                self.loadupberryfile(name)

    def save_file(self):
        self.text_window.save_file()

    def run_project(self):
        if (self.text_window.underlying_object_exists):
            self.text_window.save_file()
        self.threadpool.start(Worker(self.manager.project.run_project))

    @pyqtSlot()
    def finished_find(self):
        print('Finished finding berries')
        # sw.setWindowFlags()
        self.picture_window.set_picture(self.manager.current_image())
        self.picture_window.fit_window()
        self.picture_window.show_berries(self.manager.berry_map)
        self.picture_window.show()

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
        filepath = dialog.getExistingDirectory(self,
                                               'Choose existing project or create a new folder',
                                               '/msys64/home/mike/code/Phase_2/projects')
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
