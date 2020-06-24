import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class Main(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # displays "status" in bar at bottom of window
        self.statusBar().showMessage("Welcome")

        act = self.makeActions()

        # creates a menu bar with an option to close the window
        menubar = self.menuBar()
        # Mac OS deals with menus differently, so disable native handling
        if sys.platform == "darwin":
            menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(act["exit"])

        # create a toolbar
        self.toolbar = self.addToolBar("Exit")
        _ = Qt.Orientations
        self.toolbar.setLayoutDirection(Qt.Orientations)
        self.toolbar.addAction(act["exit"])

        # get the bounds of the available screen space        
        cp = QDesktopWidget().availableGeometry()

        # set frame to 70% of available window, centered
        self.setGeometry(cp.topLeft().x()+cp.width()*.15, cp.topLeft().y()+cp.height()*.15, cp.width()*.7, cp.height()*.7)

        self.setWindowTitle("Ghost Hunters")
        self.setWindowIcon(QIcon("Images/logo.png"))

    def makeActions(self) -> dict:
        """ Defines all the actions that this Qt application uses 
        
        Returns: dict with entries
            'exit' : an exit action
        """

        ret = {}

        # creates an action to close window
        tmp = QAction(QIcon("Images/exit.png"), "&Exit", self)
        tmp.setShortcut("Ctrl+Q")
        tmp.setStatusTip("Exit Application")
        tmp.triggered.connect(qApp.quit)
        ret["exit"] = tmp


        return ret

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Main()
    ex.show()

    sys.exit(app.exec_())