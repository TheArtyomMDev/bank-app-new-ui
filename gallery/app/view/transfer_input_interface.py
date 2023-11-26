# coding:utf-8
import math

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QButtonGroup, QCompleter, QTextEdit, QHBoxLayout, QLabel, \
    QSizePolicy
from qfluentwidgets import (Action, DropDownPushButton, DropDownToolButton, PushButton, ToolButton, PrimaryPushButton,
                            HyperlinkButton, ComboBox, RadioButton, CheckBox, Slider, SwitchButton, EditableComboBox,
                            ToggleButton, RoundMenu, FluentIcon, SplitPushButton, SplitToolButton,
                            PrimarySplitToolButton,
                            PrimarySplitPushButton, PrimaryDropDownPushButton, PrimaryToolButton,
                            PrimaryDropDownToolButton,
                            ToggleToolButton, TransparentDropDownPushButton, TransparentPushButton,
                            TransparentToggleToolButton,
                            TransparentTogglePushButton, TransparentDropDownToolButton, TransparentToolButton,
                            PillPushButton, PillToolButton, LineEdit, SearchLineEdit, FlowLayout, DoubleSpinBox,
                            TitleLabel, InfoBar, InfoBarPosition)

from helpers import InstanceHolders
from helpers.ConfigManager import ConfigManager
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet
from ..common.translator import Translator
from ..components.money_card import MoneyCard
from ..components.sample_card import SampleCard, SampleCardView

api = InstanceHolders.api
config = ConfigManager()


class TransferMoneyInputInterface(GalleryInterface):
    """ Basic input interface """

    receiver = ""

    def set_receiver(self, receiver):
        self.receiver = receiver

        if self.receiver in self.users_tags:
            self.pb.setEnabled(True)
        else:
            self.pb.setEnabled(False)

    def __init__(self, parent=None):
        translator = Translator()
        self.users = api.get_users()
        self.users_tags = {user["tag"]: user for user in self.users}

        super().__init__(
            title=translator.transfer,
            subtitle="",
            parent=parent
        )
        self.setObjectName('transferInputInterface')

        self.lineEdit = SearchLineEdit(self)
        self.lineEdit.setPlaceholderText(self.tr('Receiver'))
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setFixedWidth(300)
        self.lineEdit.textChanged.connect(lambda: self.set_receiver(self.lineEdit.text()))

        completer = QCompleter(self.users_tags, self.lineEdit)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setMaxVisibleItems(10)
        self.lineEdit.setCompleter(completer)

        self.addExampleCard(
            "",
            self.lineEdit,
        )

        main_widget = QWidget()
        lay = QVBoxLayout(main_widget)
        label = TitleLabel("Choose card to transfer from", parent=None)
        lay.addWidget(label)

        widget = QWidget()
        layout = QHBoxLayout(widget)

        cur_balance = api.get_balance()
        for _ in range(1):
            layout.addWidget(MoneyCard(icon=":/gallery/images/controls/Card.png",
                                       title="**** 1256",
                                       content=str(cur_balance)))

        layout.addStretch()
        lay.addWidget(widget)

        self.money_input = DoubleSpinBox(self)
        self.money_input.setRange(1, cur_balance)
        self.money_input.setMaximumWidth(200)
        lay.addSpacing(10)
        lay.addWidget(self.money_input)

        self.addExampleCard(
            '',
            main_widget
        )

        self.pb = PrimaryPushButton(self.tr('Proceed'))
        self.pb.setEnabled(False)
        self.pb.clicked.connect(self.do_proceed)
        self.addExampleCard(
            '',
            self.pb,
        )

    def do_proceed(self):
        api.transfer(self.users_tags[self.receiver]['uid'], self.money_input.value(), "default message", self.on_transfer_finished)

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
                parent=self
            )
        else:
            InfoBar.error(
                title='Transfer failed',
                content=str(res["reason"]),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,
                parent=self
            )