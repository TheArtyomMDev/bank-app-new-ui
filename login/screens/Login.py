from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from email_validator import validate_email, EmailNotValidError
from qfluentwidgets import PasswordLineEdit, LineEdit, PrimaryPushButton, BodyLabel

from api.ServerApi import ServerApi


class PasswordNotValidError(Exception):
    pass

class LoginWidget(QWidget):
    def __init__(self, onLogged):
        super().__init__()

        self.onLogged = onLogged

        lay = QVBoxLayout()

        email = LineEdit()
        email.setPlaceholderText("Email")

        lay.addWidget(email)

        password = PasswordLineEdit()
        password.setPlaceholderText("Password")
        lay.addWidget(password)

        self.error = BodyLabel("", parent=None)
        self.error.setMaximumHeight(40)
        self.error.setWordWrap(True)
        self.error.setStyleSheet("color: red; font-size: 12px; font-weight: bold; text-align: center;")
        lay.addWidget(self.error)

        lay.addSpacing(50)

        self.btn_login = PrimaryPushButton('Login')
        self.btn_login.clicked.connect(lambda: self.login(email.text(), password.text()))
        lay.addWidget(self.btn_login)

        self.setLayout(lay)

    def set_error(self, error):
        self.error.setText(error)

        if error == "":
            self.error.setVisible(False)
        else:
            self.error.setVisible(True)

    def login(self, email, password):
        try:
            validate_email(email, check_deliverability=False)

            if len(password) < 6:
                raise PasswordNotValidError("Password must be at least 6 characters long")

            self.set_error("")
            ServerApi().login(email, password, self.onLogged, self.set_error)
        except EmailNotValidError as e:
            self.set_error(str(e))
        except PasswordNotValidError as e:
            self.set_error(str(e))




