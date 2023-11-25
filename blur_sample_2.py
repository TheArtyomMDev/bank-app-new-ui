import sys

from BlurWindow.blurWindow import blur
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget


class SuperBlurred(QWidget):
    def __init__(self):
        # super(MainWindow, self).__init__()
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(500, 400)

        hWnd = self.winId()
        blur(hWnd)

        self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = SuperBlurred()
    mw.show()
    sys.exit(app.exec_())
