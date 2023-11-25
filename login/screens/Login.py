import asyncio

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel
from qfluentwidgets import PasswordLineEdit, LineEdit, PrimaryPushButton, BodyLabel

from api.ServerApi import ServerApi


class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()

        lay = QVBoxLayout()

        email = LineEdit()
        email.setPlaceholderText("Email")

        lay.addWidget(email)

        password = PasswordLineEdit()
        password.setPlaceholderText("Password")
        lay.addWidget(password)

        self.error = BodyLabel("", parent=None)
        self.error.setMaximumHeight(20)
        lay.addWidget(self.error)

        lay.addSpacing(50)

        self.btn_login = PrimaryPushButton('Login')
        self.btn_login.clicked.connect(lambda: self.login(email.text(), password.text()))
        lay.addWidget(self.btn_login)

        self.setLayout(lay)

    def set_error(self):
        self.error.setText("Error")

    def login(self, email, password):
        async def main():
            result = ServerApi().login(email, password)
            print("Got result:", result)

        asyncio.run(main())
