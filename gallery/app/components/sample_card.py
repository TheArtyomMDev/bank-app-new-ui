# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from qfluentwidgets import IconWidget, TextWrap, FlowLayout, CardWidget

from ..common.signal_bus import signal_bus
from ..common.style_sheet import StyleSheet


class SampleCard(CardWidget):
    """ Sample card """

    def __init__(self, icon, title, content, routeKey, index, parent=None):
        super().__init__(parent=parent)

        self.index = index
        self.routekey = routeKey

        self.setFixedSize(198, 220)
        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 28, False)[0], self)

        self.iconWidget.setFixedSize(120, 120)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(24, 24, 0, 13)
        self.vBoxLayout.addWidget(self.iconWidget, alignment=Qt.AlignCenter)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        signal_bus.switch_to_sample_card.emit(self.routekey, self.index)


class SampleCardView(QWidget):
    """ Sample card view """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout()

        self.vBoxLayout.setContentsMargins(36, 0, 36, 0)
        self.vBoxLayout.setSpacing(10)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setHorizontalSpacing(12)
        self.flowLayout.setVerticalSpacing(12)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addLayout(self.flowLayout, 1)

        self.titleLabel.setObjectName('viewTitleLabel')
        StyleSheet.SAMPLE_CARD.apply(self)

    def addSampleCard(self, icon, title, content, routeKey, index):
        card = SampleCard(icon, title, content, routeKey, index, self)
        self.flowLayout.addWidget(card)
