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

    def __init__(self, on_logged):
        super().__init__()
        self.setFixedSize(400, 400)

        def on_my_logged(token):
            on_logged(token)
            self.destroy()

        self.pivot = SegmentedWidget(self)
        self.stacked_widget = QStackedWidget(self)
        self.v_box_layout = QVBoxLayout(self)

        self.login_screen = LoginWidget(on_my_logged)
        self.signup_screen = SignupWidget(on_my_logged)
        self.email_screen = EmailWidget(on_my_logged)

        # add items to pivot
        self.addSubInterface(self.login_screen, 'login_screen', 'Login')
        self.addSubInterface(self.signup_screen, 'signup_screen', 'SignUp')
        self.addSubInterface(self.email_screen, 'email_screen', 'Email')

        self.v_box_layout.addWidget(self.pivot)
        self.v_box_layout.addWidget(self.stacked_widget)
        self.v_box_layout.setContentsMargins(30, 10, 30, 30)

        self.stacked_widget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stacked_widget.setCurrentWidget(self.login_screen)
        self.pivot.setCurrentItem(self.login_screen.objectName())

        self.setObjectName('view')
        StyleSheet.GALLERY_INTERFACE.apply(self)

    def addSubInterface(self, widget: QWidget, objectName, text):
        widget.setObjectName(objectName)

        self.stacked_widget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stacked_widget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stacked_widget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())