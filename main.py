# enable dpi scale

import pyqt5ac

from api.ServerApi import ServerApi
from helpers import InstanceHolders
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
    api.set_token(token)
    config.set_tag(api.get_tag())
    MainWindow().show()


config = ConfigManager()
api = InstanceHolders.api

if config.is_logged():
    tag = api.get_tag()
    print("TAG: " + tag)
    config.set_tag(tag)

    w = MainWindow()
else:
    w = LoginWindow(onLogged)

w.show()

app.exec_()
