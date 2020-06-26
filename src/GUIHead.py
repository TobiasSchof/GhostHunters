import sys, os
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QAction, qApp, QToolBar, QPushButton, QWidget, QDialog, QDialogButtonBox, QMessageBox, QGridLayout, QLineEdit, QSlider, QLabel
from PyQt5.QtGui import QIcon, QPainter, QPen, QColor, QPalette, QPolygon, QDoubleValidator
from PyQt5.QtCore import Qt, QSize, QPoint

from core import Boundary

IMAGES = os.path.dirname(os.path.dirname(__file__)) + "/Images/"

class Wedge(QWidget):
    def __init__(self, *args, **kw_args):
        super(Wedge, self).__init__(*args, **kw_args)
        self.angle = 0

        g = self.geometry()

        self.bl = QPoint(0, g.height()-1)
        self.br = QPoint(g.width()-1, g.height()-1)
        self.tl = QPoint(0, 0)
        self.tr = QPoint(g.width()-1, 0)
        self.wedgePt = QPoint(g.width()-1, 0)

    def calc_wedgePt(self) -> QPoint:
        x = np.tan(self.angle*(np.pi/180))*(self.br.y() - self.tr.y())

        return QPoint(int(self.tr.x()-x), 0)

    def paintEvent(self, eventPaintQEvent):
        g = self.geometry()
        
        self.bl = QPoint(0, g.height()-1)
        self.br = QPoint(g.width()-1, g.height()-1)
        self.tl = QPoint(0, 0)
        self.tr = QPoint(g.width()-1, 0)
        self.wedgePt = self.calc_wedgePt()
        
        myQP = QPainter(self)

        pen = QPen()
        pen.setWidth(3)
        pen.setColor(Qt.lightGray)
        pen.setDashPattern([5,5])
        myQP.setPen(pen)
        myQP.drawLine(self.wedgePt, self.tr)
        myQP.drawLine(self.tr, self.br)

        pen.setColor(Qt.black)
        pen.setDashPattern([1,0])
        myQP.setPen(pen)

        myQP.drawLine(self.bl, self.br)
        myQP.drawLine(self.bl, self.tl)
        myQP.drawLine(self.tl, self.wedgePt)
        myQP.drawLine(self.wedgePt, self.br)

class WedgePopup1(QDialog):
    def __init__(self, *args, **kw_args):
        super(WedgePopup1, self).__init__(*args, **kw_args)

        self.setWindowTitle("Wedge angle selection")

        self.ok = False
        self.a = QLineEdit("", self)
        self.a.setValidator(QDoubleValidator(0, 45, 3, notation=QDoubleValidator.StandardNotation))
        self.a.setToolTip("Wedge angle in degrees")
        self.a.textChanged.connect(self.wedge_update)

        grid = QGridLayout()
        self.setLayout(grid)

        grid.setRowMinimumHeight(2, 60)
        grid.setRowMinimumHeight(3, 40)
        grid.setRowMinimumHeight(4, 40)
        grid.setRowMinimumHeight(5, 60)
        grid.setColumnMinimumWidth(0, 105)
        grid.setColumnMinimumWidth(1, 100)
        grid.setColumnMinimumWidth(2, 105)
        self.wedge = Wedge()
        grid.addWidget(self.wedge, 2, 0, 4, 3)

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksAbove)
        slider.setRange(0, 45)
        slider.setTickInterval(5)
        slider.setValue(45)
        slider.valueChanged.connect(self.update_a)
        grid.addWidget(slider, 1, 1)
        self.a.setAlignment(Qt.AlignCenter)
        self.a.setText(str(45-slider.value()))
        self.a.setToolTip("Wedge angle in degrees")
        grid.addWidget(self.a, 0, 1)

        self.ref_idx = QLineEdit("", self)
        self.ref_idx.setValidator(QDoubleValidator(0, 3, 4, notation = QDoubleValidator.StandardNotation))
        self.ref_idx.setAlignment(Qt.AlignCenter)
        self.ref_idx.setText("1.0")
        grid.addWidget(self.ref_idx, 4, 3)
        grid.addWidget(QLabel("Refractive index:"), 3, 3)

        btn_c = QPushButton("Cancel", self)
        btn_c.clicked.connect(self.close)
        grid.addWidget(btn_c, 7, 0)
        btn_a = QPushButton("Next", self)
        btn_a.clicked.connect(self.make)
        grid.addWidget(btn_a, 7, 3)

    def make(self, *args, **kw_args):
        self.ok = True
        self.close()

    def update_a(self, value):
        self.a.setText(str(45-value))
    
    def wedge_update(self, value):

        if value == "":
            self.wedge.andgle = "0"
        else:
            self.wedge.angle = float(value)
        
        self.wedge.update()

class WedgePopup2(QDialog):

    def __init__(self, wedge:Wedge):
        super(WedgePopup2, self).__init__()

        self.setWindowTitle("Transmission coefficients")

        self.wedge = wedge

        grid = QGridLayout()

        grid.setRowMinimumHeight(1, 135)
        grid.setRowMinimumHeight(2, 30)
        grid.setRowMinimumHeight(3, 135)
        grid.setColumnMinimumWidth(1, 140)
        grid.setColumnMinimumWidth(2, 30)
        grid.setColumnMinimumWidth(3, 140)
        grid.setRowMinimumHeight(5, 40)

        grid.addWidget(self.wedge, 1, 1, 3, 3)

        self.ok = False

        self.l = QLineEdit("", self)
        self.l.setValidator(QDoubleValidator(0.0, 1.0, 3, notation=QDoubleValidator.StandardNotation))
        self.l.setToolTip("Ratio of light that the left face transmits")
        self.l.setAlignment(Qt.AlignCenter)
        self.l.setText("1.0")

        self.r = QLineEdit("", self)
        self.r.setValidator(QDoubleValidator(0.0, 1.0, 3, notation=QDoubleValidator.StandardNotation))
        self.r.setToolTip("Ratio of light that the right face transmits")
        self.r.setAlignment(Qt.AlignCenter)
        self.r.setText("1.0")

        self.t = QLineEdit("", self)
        self.t.setValidator(QDoubleValidator(0.0, 1.0, 3, notation=QDoubleValidator.StandardNotation))
        self.t.setToolTip("Ratio of light that the top face transmits")
        self.t.setAlignment(Qt.AlignCenter)
        self.t.setText("1.0")

        self.b = QLineEdit("", self)
        self.b.setValidator(QDoubleValidator(0.0, 1.0, 3, notation=QDoubleValidator.StandardNotation))
        self.b.setToolTip("Ratio of light that the bottom face transmits")
        self.b.setAlignment(Qt.AlignCenter)
        self.b.setText("1.0")

        grid.addWidget(self.l, 2, 0, 1, 1)
        grid.addWidget(self.r, 2, 4, 1, 1)
        grid.addWidget(self.t, 0, 2, 1, 1)
        grid.addWidget(self.b, 4, 2, 1, 1)

        btn_c = QPushButton("Discard", self)
        btn_c.clicked.connect(self.close)
        grid.addWidget(btn_c, 6, 1)
        btn_a = QPushButton("Create", self)
        btn_a.clicked.connect(self.make)
        grid.addWidget(btn_a, 6, 3)

        self.setLayout(grid)

    def make(self, *args, **kw_args):
        self.ok = True
        self.close()    

class Main(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initUI()
        self.bounds = []

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
        w_a = WedgePopup1()
        w_a.setMinimumSize(200, 200)
        w_a.exec_()
        if w_a.ok:
            w_c = WedgePopup2(w_a.wedge)
            w_c.setMinimumSize(200, 200)
            w_c.exec_()
            if w_c.ok:
                ref_idx = 0 if w_a.ref_idx.text() == "" else float(w_a.ref_idx.text())
                self.bounds.append(Boundary(list(w_c.wedge.tl), list(w_c.wedge.bl), (0 if w_c.l.text() == "" else float(w_c.l.text())), ref_idx))
                self.bounds.append(Boundary(list(w_c.wedge.tl), list(w_c.wedge.tr), (0 if w_c.t.text() == "" else float(w_c.t.text())), ref_idx))
                self.bounds.append(Boundary(list(w_c.wedge.tr), list(w_c.wedge.br), (0 if w_c.r.text() == "" else float(w_c.lrtext())), ref_idx))
                self.bounds.append(Boundary(list(w_c.wedge.bl), list(w_c.wedge.br), (0 if w_c.b.text() == "" else float(w_c.b.text())), ref_idx))
            w_c.deleteLater()
        w_a.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Main()
    ex.show()

    sys.exit(app.exec_())