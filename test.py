import sys

from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont("SansSerif", 10))
        self.setToolTip("This is a <b>GHOST HUNTERS</b>")

        self.statusBar()
        # create a button that calls doSomething when it's clicked
        btn = QPushButton("Button", self)
        btn.clicked.connect(doSomething)
        btn.setToolTip("This is a button?")
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        # get the bounds of the available screen space        
        cp = QDesktopWidget().availableGeometry()

        # set frame to 70% of available window, centered
        self.setGeometry(cp.topLeft().x()+cp.width()*.15, cp.topLeft().y()+cp.height()*.15, cp.width()*.7, cp.height()*.7)

        self.setWindowTitle("Ghost Hunters")
        self.setWindowIcon(QIcon("logo.png"))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            event.accept()
        else:

            event.ignore()

def doSomething(*args, **kw_args):
    print(args)
    print(kw_args)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    ex = Example()
    ex.show()

    sys.exit(app.exec_())