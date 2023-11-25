# enable dpi scale

import pyqt5ac

from helpers.ConfigManager import ConfigManager
from login.loginwindow import LoginWindow

pyqt5ac.main(uicOptions='--from-imports', force=False, initPackage=True, ioPaths=[
    # ['gui/*.ui', 'generated/%%FILENAME%%_ui.py'],
    ['gallery/app/resource/resource.qrc', 'gallery/app/common/resource.py'],
    # ['modules/*/*.ui', '%%DIRNAME%%/generated/%%FILENAME%%_ui.py'],
    # ['modules/*/resources/*.qrc', '%%DIRNAME%%/generated/%%FILENAME%%_rc.py']
])

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from gallery.app.view.main_window import MainWindow
from gallery.app.common import resource

QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

app = QApplication(sys.argv)


def onLogged(token):
    config.set_token(token)
    MainWindow().show()

config = ConfigManager()

if config.is_logged():
    w = MainWindow()
else:
    w = LoginWindow(onLogged)

w.show()

app.exec_()
