from BlurWindow.blurWindow import blur
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import LineEdit, PrimaryPushButton, TitleLabel

from gallery.app.common.style_sheet import StyleSheet


class PasscodeWidget(QWidget):


    def __init__(self, help_text: str, on_passcode_entered):
        super().__init__()

        self.passcode = ""
        self.pass_fields: list[LineEdit] = []

        self.on_passcode_entered = on_passcode_entered

        self.setFixedSize(400, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        label = TitleLabel(help_text)
        label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label)

        num_layout = QHBoxLayout()

        for _ in range(4):
            password = LineEdit()
            password.setMaxLength(1)
            password.setMaximumWidth(50)
            password.setEnabled(False)
            password.setAlignment(Qt.AlignCenter)
            num_layout.addWidget(password)
            self.pass_fields.append(password)

        tmp_widget = QWidget()
        tmp_widget.setLayout(num_layout)
        main_layout.addWidget(tmp_widget)

        # cancel should be in center
        main_layout.addSpacing(20)
        cancel = PrimaryPushButton("Cancel")
        cancel.setMaximumWidth(100)
        cancel.clicked.connect(lambda: self.destroy())
        main_layout.addWidget(cancel, alignment=Qt.AlignCenter)

        self.setObjectName('view')
        StyleSheet.GALLERY_INTERFACE.apply(self)

        # blur(self.winId())

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)

        if event.text().isdigit() and len(self.passcode) < 4:
            self.passcode += event.text()
        elif event.key() == 16777219 and len(self.passcode) > 0:
            self.passcode = self.passcode[0:-1]

        for i in range(len(self.pass_fields)):
            if i < len(self.passcode):
                self.pass_fields[i].setText("⚪")
            else:
                self.pass_fields[i].setText("")

        if len(self.passcode) == 4:
            self.on_passcode_entered(self.passcode)
