import sys, os
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QAction, qApp, QToolBar, QPushButton, QWidget, QDialog, QDialogButtonBox, QMessageBox, QGridLayout, QTextEdit, QSlider, QLabel
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import Qt, QSize

IMAGES = os.path.dirname(os.path.dirname(__file__)) + "/Images/"
print(IMAGES)

class SolidPopup(QDialog):
    def __init__(self, *args, **kw_args):
        super(SolidPopup, self).__init__(*args, **kw_args)

        self.ok = False
        self.dims_label = QLabel("", self)

        grid = QGridLayout()
        self.setLayout(grid)

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksAbove)
        slider.setRange(3, 10)
        slider.setTickInterval(1)
        slider.valueChanged.connect(self.update_dim)
        grid.addWidget(slider, 1, 1)
        self.dims_label.setAlignment(Qt.AlignCenter)
        self.dims_label.setText(str(slider.value()))
        grid.addWidget(self.dims_label, 0, 1)

        dims = QLabel()
        dims.text()

        btn = QPushButton("Add", self)
        btn.clicked.connect(self.make)
        grid.addWidget(btn, 3, 1)

    def make(self, *args, **kw_args):
        self.ok = True
        self.close()

    def update_dim(self, value):
        self.dims_label.setText(str(value))

class Main(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # displays "status" in bar at bottom of window
        self.statusBar().showMessage("Welcome")

        # creates an action to close window
        exitAct = QAction(QIcon(IMAGES+"exit.png"), "&Exit", self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.setStatusTip("Exit Application")
        exitAct.triggered.connect(qApp.quit)
        # creates a menu bar with an option to close the window
        menubar = self.menuBar()
        # Mac OS deals with menus differently, so disable native handling
        if sys.platform == "darwin":
            menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(exitAct)

        # create a toolbar on the right of the screen
        self.toolbar = QToolBar("System setup")
        self.addToolBar(Qt.RightToolBarArea, self.toolbar)

        # get the size of a section on the toolbar
        section = int(self.toolbar.height()/7)

        # add a button to the toolbar to create a mirror
        btn = QPushButton("", self)
        btn.setIcon(QIcon(IMAGES+"mirror.png"))
        btn.setIconSize(QSize(section, section))
        btn.clicked.connect(self.add_mirror)
        btn.setStatusTip("Add a mirror to the system")
        
        self.toolbar.addWidget(btn)

        # add a button to the toolbar to create a solid
        btn = QPushButton("", self)
        btn.setIcon(QIcon(IMAGES+"solid.png"))
        btn.setIconSize(QSize(section, section))
        btn.clicked.connect(self.add_solid)
        btn.setStatusTip("Add an n-sided solid to the system")

        self.toolbar.addWidget(btn)

        # get the bounds of the available screen space        
        cp = QDesktopWidget().availableGeometry()

        # set frame to 70% of available window, centered
        self.setGeometry(int(cp.topLeft().x()+cp.width()*.15), int(cp.topLeft().y()+cp.height()*.15), int(cp.width()*.7), int(cp.height()*.7))

        self.setWindowTitle("Ghost Hunters")
        self.setWindowIcon(QIcon(IMAGES+"logo.png"))

    def add_mirror(self):
        """ adds a mirror to the system """
        print("mirror made")

    def add_solid(self):
        """ adds an n-sided solid to the system """
        print("solid made")
        w = SolidPopup()
        w.setGeometry(200, 200, 200, 200)
        w.setAttribute(Qt.WA_DeleteOnClose)
        w.exec_()
        print(w.ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Main()
    ex.show()

    sys.exit(app.exec_())