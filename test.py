import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

def main():
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle("Test")
    w.setWindowIcon(QIcon("logo.png"))
    w.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()