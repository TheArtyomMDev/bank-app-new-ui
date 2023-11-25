

# enable dpi scale

import pyqt5ac

pyqt5ac.main(uicOptions='--from-imports', force=False, initPackage=True, ioPaths=[
        # ['gui/*.ui', 'generated/%%FILENAME%%_ui.py'],
        ['gallery/app/resource/resource.qrc', 'gallery/app/common/resource.py'],
        # ['modules/*/*.ui', '%%DIRNAME%%/generated/%%FILENAME%%_ui.py'],
        # ['modules/*/resources/*.qrc', '%%DIRNAME%%/generated/%%FILENAME%%_rc.py']
    ])

import os
import sys

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from gallery.app.common.config import cfg
from gallery.app.view.main_window import MainWindow

QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()
