import os
import sys

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from gallery.app.common.config import cfg
from gallery.app.view.main_window import MainWindow

# enable dpi scale

QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()
