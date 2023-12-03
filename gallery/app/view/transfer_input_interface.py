# coding:utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCompleter, QHBoxLayout
from qfluentwidgets import (PrimaryPushButton,
                            LineEdit, SearchLineEdit, DoubleSpinBox,
                            TitleLabel, InfoBar, InfoBarPosition)

from helpers import InstanceHolders
from helpers.ConfigManager import ConfigManager
from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..components.money_card import MoneyCard

api = InstanceHolders.api
config = ConfigManager()


class TransferMoneyInputInterface(GalleryInterface):
    receiver = ""

    def set_receiver(self, receiver):
        self.receiver = receiver

        if self.receiver in self.users_tags and self.cur_balance >= 1:
            self.pb.setEnabled(True)
        else:
            self.pb.setEnabled(False)

    def __init__(self, parent=None):
        translator = Translator()
        self.parent = parent
        self.users = api.get_users()
        self.users_tags = {user["tag"]: user for user in self.users}

        super().__init__(
            title=translator.transfer,
            subtitle="",
            parent=parent
        )
        self.setObjectName('transferInputInterface')

        self.search_line_edit = SearchLineEdit(self)
        self.search_line_edit.setPlaceholderText(self.tr('Receiver'))
        self.search_line_edit.setClearButtonEnabled(True)
        self.search_line_edit.setFixedWidth(300)
        self.search_line_edit.textChanged.connect(lambda: self.set_receiver(self.search_line_edit.text()))

        completer = QCompleter(self.users_tags, self.search_line_edit)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setMaxVisibleItems(10)
        self.search_line_edit.setCompleter(completer)

        self.addExampleCard(
            "",
            self.search_line_edit,
        )

        main_widget = QWidget()
        lay = QVBoxLayout(main_widget)
        label = TitleLabel("Choose card to transfer from", parent=None)
        lay.addWidget(label)

        widget = QWidget()
        layout = QHBoxLayout(widget)

        self.cur_balance = api.get_balance()
        for _ in range(1):
            layout.addWidget(MoneyCard(icon=":/gallery/images/controls/Card.png",
                                       title="**** 1256",
                                       content=str(self.cur_balance)))

        layout.addStretch()
        lay.addWidget(widget)

        self.money_input = DoubleSpinBox(self)

        self.money_input.setRange(1, self.cur_balance)
        self.money_input.setMaximumWidth(200)

        if self.cur_balance < 1:
            self.money_input.setEnabled(False)

        lay.addSpacing(10)
        lay.addWidget(self.money_input)

        self.addExampleCard(
            '',
            main_widget
        )

        lay = QVBoxLayout()

        self.message = LineEdit(self)
        self.message.setPlaceholderText("Your Message")

        self.pb = PrimaryPushButton(self.tr('Proceed'))
        self.pb.setEnabled(False)
        self.pb.setMaximumWidth(200)
        self.pb.clicked.connect(self.do_proceed)

        lay.addWidget(self.message)
        lay.addWidget(self.pb)

        tmp_widget = QWidget()
        tmp_widget.setLayout(lay)
        tmp_widget.setFixedWidth(500)

        self.addExampleCard(
            '',
            tmp_widget,
        )

    def do_proceed(self):
        api.transfer(
            self.users_tags[self.receiver]['uid'],
            self.money_input.value(),
            self.message.text(),
            self.on_transfer_finished
        )

    def on_transfer_finished(self, res):
        print(res)

        if res["status"] == "OK":
            InfoBar.success(
                title='Transfer success',
                content='Money left: ' + str(res["data"]["balance"]),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=5000,
                parent=self.parent
            )
        else:
            InfoBar.error(
                title='Transfer failed',
                content=str(res["reason"]),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,
                parent=self.parent
            )
