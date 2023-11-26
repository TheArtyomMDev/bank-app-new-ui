# coding:utf-8
import math

from PyQt5.QtCore import Qt, QSize
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

class TableFrame(TableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(3)
        self.setHorizontalHeaderLabels([
            self.tr('CharCode'), self.tr('Name'), self.tr('Value'),
        ])

        self.rates = api.get_exchange_rates()["Valute"]
        self.setRowCount(len(self.rates))
        print(self.rates)
        final_rates = []

        for valute in self.rates:
            rate = self.rates[valute]
            final_rates.append([rate["CharCode"], rate["Name"], str(rate["Value"])])

        # songInfos = [
        #     ['かばん', 'aiko', 'かばん', '2004', '5:04'],
        #     ['爱你', '王心凌', '爱你', '2004', '3:39'],
        #     ['星のない世界', 'aiko', '星のない世界/横顔', '2007', '5:30'],
        #     ['横顔', 'aiko', '星のない世界/横顔', '2007', '5:06'],
        #     ['秘密', 'aiko', '秘密', '2008', '6:27'],
        #     ['シアワセ', 'aiko', '秘密', '2008', '5:25'],
        #     ['二人', 'aiko', '二人', '2008', '5:00'],
        #     ['スパークル', 'RADWIMPS', '君の名は。', '2016', '8:54'],
        #     ['なんでもないや', 'RADWIMPS', '君の名は。', '2016', '3:16'],
        #     ['前前前世', 'RADWIMPS', '人間開花', '2016', '4:35'],
        #     ['恋をしたのは', 'aiko', '恋をしたのは', '2016', '6:02'],
        #     ['夏バテ', 'aiko', '恋をしたのは', '2016', '4:41'],
        #     ['もっと', 'aiko', 'もっと', '2016', '4:50'],
        #     ['問題集', 'aiko', 'もっと', '2016', '4:18'],
        #     ['半袖', 'aiko', 'もっと', '2016', '5:50'],
        #     ['ひねくれ', '鎖那', 'Hush a by little girl', '2017', '3:54'],
        #     ['シュテルン', '鎖那', 'Hush a by little girl', '2017', '3:16'],
        #     ['愛は勝手', 'aiko', '湿った夏の始まり', '2018', '5:31'],
        #     ['ドライブモード', 'aiko', '湿った夏の始まり', '2018', '3:37'],
        #     ['うん。', 'aiko', '湿った夏の始まり', '2018', '5:48'],
        #     ['キラキラ', 'aikoの詩。', '2019', '5:08', 'aiko'],
        #     ['恋のスーパーボール', 'aiko', 'aikoの詩。', '2019', '4:31'],
        #     ['磁石', 'aiko', 'どうしたって伝えられないから', '2021', '4:24'],
        #     ['食べた愛', 'aiko', '食べた愛/あたしたち', '2021', '5:17'],
        #     ['列車', 'aiko', '食べた愛/あたしたち', '2021', '4:18'],
        #     ['花の塔', 'さユり', '花の塔', '2022', '4:35'],
        #     ['夏恋のライフ', 'aiko', '夏恋のライフ', '2022', '5:03'],
        #     ['あかときリロード', 'aiko', 'あかときリロード', '2023', '4:04'],
        #     ['荒れた唇は恋を失くす', 'aiko', '今の二人をお互いが見てる', '2023', '4:07'],
        #     ['ワンツースリー', 'aiko', '今の二人をお互いが見てる', '2023', '4:47'],
        # ]

        # songInfos += songInfos
        for i, songInfo in enumerate(final_rates):
            for j in range(3):
                self.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.setFixedSize(625, 440)
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
            TableFrame(),
        )
