# coding:utf-8
import math

from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QButtonGroup, QCompleter, QTextEdit, QHBoxLayout, QLabel, \
    QTableWidgetItem
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
                            TitleLabel, TableWidget)

from helpers import InstanceHolders
from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet
from ..common.translator import Translator
from ..components.sample_card import SampleCard, SampleCardView

api = InstanceHolders.api


class ExchangeRatesTable(TableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.th = QThread()
        self.rates = []

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(3)
        self.setHorizontalHeaderLabels([
            self.tr('CharCode'), self.tr('Name'), self.tr('Value'),
        ])

        class UpdateTransactions(QObject):
            finished = pyqtSignal()

            def startWork(self2):
                self.rates = api.get_exchange_rates()["Valute"]
                self2.finished.emit()

        self.worker = UpdateTransactions()

        self.worker.moveToThread(self.th)

        self.th.started.connect(self.worker.startWork)
        self.worker.finished.connect(self.th.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.update_table)

        self.th.start()

    def update_table(self):
        self.setRowCount(len(self.rates))
        print(self.rates)
        final_rates = []

        for valute in self.rates:
            rate = self.rates[valute]
            final_rates.append([rate["CharCode"], rate["Name"], str(rate["Value"])])

        for i, songInfo in enumerate(final_rates):
            for j in range(3):
                self.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.setFixedSize(500, 440)
        self.resizeColumnsToContents()


class ExchangeInputInterface(GalleryInterface):
    def __init__(self, parent=None):
        translator = Translator()
        super().__init__(
            title=translator.exchange,
            subtitle="",
            parent=parent
        )
        self.setObjectName('exchangeInputInterface')

        self.addExampleCard(
            "",
            ExchangeRatesTable(),
        )
