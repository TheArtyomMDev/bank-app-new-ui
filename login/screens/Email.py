from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from email_validator import validate_email, EmailNotValidError
from qfluentwidgets import PasswordLineEdit, LineEdit, PrimaryPushButton, BodyLabel

from api.ServerApi import ServerApi


class PasswordNotValidError(Exception):
    pass


class EmailWidget(QWidget):
    def __init__(self, on_logged):
        super().__init__()

        self.onLogged = on_logged

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

        self.message_box = BodyLabel("", parent=None)
        self.message_box.setMaximumHeight(40)
        self.message_box.setWordWrap(True)
        lay.addWidget(self.message_box)

        lay.addSpacing(50)

        self.btn_login = PrimaryPushButton('Login')
        self.btn_login.clicked.connect(lambda: self.login(email.text(), password.text()))
        lay.addWidget(self.btn_login)

        self.setLayout(lay)

    def set_error(self, error):
        self.message_box.setText(error)
        self.message_box.setStyleSheet("color: red; font-size: 12px; font-weight: bold; text-align: center;")

        if error == "":
            self.message_box.setVisible(False)
        else:
            self.message_box.setVisible(True)

    def login(self, email, otp):
        try:
            validate_email(email, check_deliverability=False)
            self.set_error("")
            ServerApi().verify_otp(email, otp, self.onLogged, self.set_error)
        except EmailNotValidError as e:
            self.set_error(str(e))

    def set_email_status(self):
        self.message_box.setText("Email sent. Check your inbox")
        self.message_box.setStyleSheet("color: green; font-size: 12px; font-weight: bold; text-align: center;")

        self.message_box.setVisible(True)

    def send_otp(self, email):
        try:
            validate_email(email, check_deliverability=False)
            self.set_error("")
            ServerApi().send_otp(email, self.set_email_status, self.set_error)
        except EmailNotValidError as e:
            self.set_error(str(e))
