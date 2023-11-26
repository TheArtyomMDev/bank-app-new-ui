from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout
from email_validator import validate_email, EmailNotValidError
from qfluentwidgets import PasswordLineEdit, LineEdit, PrimaryPushButton, BodyLabel

from api.ServerApi import ServerApi


class PasswordNotValidError(Exception):
    pass

class EmailWidget(QWidget):
    def __init__(self, onLogged):
        super().__init__()

        self.onLogged = onLogged

        lay = QVBoxLayout()

        email = LineEdit()
        email.setPlaceholderText("Email")

        lay.addWidget(email)

        otp_layout = QHBoxLayout()
        password = PasswordLineEdit()
        password.setPlaceholderText("OTP")
        otp_layout.addWidget(password)
        self.btn_otp = PrimaryPushButton('Send OTP')
        self.btn_otp.clicked.connect(lambda: self.send_otp(email.text()))
        otp_layout.addWidget(self.btn_otp)

        lay.addLayout(otp_layout)


        self.messageBox = BodyLabel("", parent=None)
        self.messageBox.setMaximumHeight(40)
        self.messageBox.setWordWrap(True)
        lay.addWidget(self.messageBox)

        lay.addSpacing(50)

        self.btn_login = PrimaryPushButton('Login')
        self.btn_login.clicked.connect(lambda: self.login(email.text(), password.text()))
        lay.addWidget(self.btn_login)

        self.setLayout(lay)

    def set_error(self, error):
        self.messageBox.setText(error)
        self.messageBox.setStyleSheet("color: red; font-size: 12px; font-weight: bold; text-align: center;")

        if error == "":
            self.messageBox.setVisible(False)
        else:
            self.messageBox.setVisible(True)

    def login(self, email, otp):
        try:
            validate_email(email, check_deliverability=False)
            self.set_error("")
            ServerApi().verify_otp(email, otp, self.onLogged, self.set_error)
        except EmailNotValidError as e:
            self.set_error(str(e))

    def set_email_status(self):
        self.messageBox.setText("Email sent. Check your inbox")
        self.messageBox.setStyleSheet("color: green; font-size: 12px; font-weight: bold; text-align: center;")

        self.messageBox.setVisible(True)

    def send_otp(self, email):
        try:
            validate_email(email, check_deliverability=False)
            self.set_error("")
            ServerApi().send_otp(email, self.set_email_status, self.set_error)
        except EmailNotValidError as e:
            self.set_error(str(e))




