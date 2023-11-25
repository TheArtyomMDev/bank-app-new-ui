from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel
from qfluentwidgets import PasswordLineEdit, LineEdit, PrimaryPushButton, BodyLabel


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
        self.btn_login.clicked.connect(self.set_error)
        lay.addWidget(self.btn_login)

        self.setLayout(lay)

    def set_error(self):
        self.error.setText("Error")