import sys, os
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QAction, qApp, QToolBar, QPushButton, QWidget, QDialog, QDialogButtonBox, QMessageBox, QGridLayout, QLineEdit, QSlider, QLabel
from PyQt5.QtGui import QIcon, QPainter, QPen, QColor, QPalette, QPolygon
from PyQt5.QtCore import Qt, QSize, QPoint

IMAGES = os.path.dirname(os.path.dirname(__file__)) + "/Images/"
print(IMAGES)

class Wedge(QWidget):
    def __init__(self, *args, **kw_args):
        super(Wedge, self).__init__(*args, **kw_args)
        self.angle = 0

    def calc_wedgePt(self) -> QPoint:
        g = self.geometry()
        x = np.tan(self.angle*(np.pi/180))*g.height()

        return QPoint(int(g.width()-1-x), 0)

    def paintEvent(self, eventPaintQEvent):
        g = self.geometry()
        
        bl = QPoint(0, g.height()-1)
        br = QPoint(g.width()-1, g.height()-1)
        tl = QPoint(0, 0)
        tr = QPoint(g.width()-1, 0)
        wedgePt = self.calc_wedgePt()
        
        myQP = QPainter(self)

        pen = QPen()
        pen.setWidth(3)
        pen.setColor(Qt.lightGray)
        pen.setDashPattern([5,5])
        myQP.setPen(pen)
        myQP.drawLine(wedgePt, tr)
        myQP.drawLine(tr, br)

        pen.setColor(Qt.black)
        pen.setDashPattern([1,0])
        myQP.setPen(pen)

        myQP.drawLine(bl, br)
        myQP.drawLine(bl, tl)
        myQP.drawLine(tl, wedgePt)
        myQP.drawLine(wedgePt, br)

class SolidPopup(QDialog):
    def __init__(self, *args, **kw_args):
        super(SolidPopup, self).__init__(*args, **kw_args)

        self.ok = False
        self.a = QLineEdit("", self)
        self.a.textChanged.connect(self.wedge_update)

        grid = QGridLayout()
        self.setLayout(grid)

        grid.setRowMinimumHeight(2, 300)
        grid.setColumnMinimumWidth(2, 100)
        grid.setColumnMinimumWidth(3, 105)
        grid.setColumnMinimumWidth(1, 105)
        self.wedge = Wedge()
        grid.addWidget(self.wedge, 2, 1, 1, 3)

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksAbove)
        slider.setRange(0, 45)
        slider.setTickInterval(5)
        slider.valueChanged.connect(self.update_a)
        grid.addWidget(slider, 1, 2)
        self.a.setAlignment(Qt.AlignCenter)
        self.a.setText(str(45-slider.value()))
        grid.addWidget(self.a, 0, 2)

        btn_c = QPushButton("Cancel", self)
        btn_c.clicked.connect(self.make)
        grid.addWidget(btn_c, 3, 0)
        btn_a = QPushButton("Add", self)
        btn_a.clicked.connect(self.make)
        grid.addWidget(btn_a, 3, 4)

    def make(self, *args, **kw_args):
        self.ok = True
        self.close()

    def update_a(self, value):
        self.a.setText(str(45-value))
    
    def wedge_update(self, value):

        if value == "":
            self.a.setText("0")
        else:
            self.wedge.angle = float(value)
            self.wedge.update()

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
        btn.setStatusTip("Add a wedge to the system")

        self.toolbar.addWidget(btn)

        # get the bounds of the available screen space        
        cp = QDesktopWidget().availableGeometry()

        # set frame to 70% of available window, centered
        self.setGeometry(int(cp.topLeft().x()+cp.width()*.15), int(cp.topLeft().y()+cp.height()*.15), int(cp.width()*.7), int(cp.height()*.7))

        self.setWindowTitle("Ghost Hunters")
        self.setWindowIcon(QIcon(IMAGES+"logo.png"))

    def add_mirror(self):
        """ adds a mirror to the system """
        pass

    def add_solid(self):
        """ adds a wedge to the system """
        w = SolidPopup()
        w.setMinimumSize(200, 200)
        w.exec_()
        print(w.ok)
        print(w.a.text())
        w.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Main()
    ex.show()

    sys.exit(app.exec_())