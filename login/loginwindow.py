# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel, QSizePolicy

from qfluentwidgets import Pivot, setTheme, Theme, SegmentedWidget, FluentIcon

from gallery.app.common.style_sheet import StyleSheet
from login.screens.Email import EmailWidget
from login.screens.Login import LoginWidget
from login.screens.Signup import SignupWidget


class LoginWindow(QWidget):

    def __init__(self, onLogged):
        super().__init__()
        self.setFixedSize(400, 400)

        def onMyLogged(token):
            onLogged(token)
            self.destroy()

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.loginScreen = LoginWidget(onMyLogged)
        self.signupScreen = SignupWidget(onMyLogged)
        self.emailScreen = EmailWidget(onMyLogged)

        # add items to pivot
        self.addSubInterface(self.loginScreen, 'songInterface', 'Login')
        self.addSubInterface(self.signupScreen, 'albumInterface', 'SignUp')
        self.addSubInterface(self.emailScreen, 'emailInterface', 'Email')

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.loginScreen)
        self.pivot.setCurrentItem(self.loginScreen.objectName())

        self.setObjectName('view')
        StyleSheet.GALLERY_INTERFACE.apply(self)

    def addSubInterface(self, widget: QWidget, objectName, text):
        widget.setObjectName(objectName)

        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


# if __name__ == '__main__':
#     # enable dpi scale
#     QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
#     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
#     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
#
#     app = QApplication(sys.argv)
#     w = LoginWindow()
#     w.show()
#     app.exec_()