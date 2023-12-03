# coding:utf-8
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QDesktopServices
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QHBoxLayout

from qfluentwidgets import IconWidget, FluentIcon, TextWrap, SingleDirectionScrollArea
from ..common.style_sheet import StyleSheet


class MoneyCard(QFrame):

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent=parent)

        # self.setFixedSize(198, 220)
        self.setFixedSize(120, 180)
        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 28, False)[0], self)

        self.__initWidget()
        self.view = QWidget(self)

    def __initWidget(self):
        self.setCursor(Qt.PointingHandCursor)

        self.iconWidget.setFixedSize(100, 100)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        # self.vBoxLayout.setContentsMargins(24, 24, 0, 13)
        self.vBoxLayout.addWidget(self.iconWidget, alignment=Qt.AlignCenter)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.titleLabel, alignment=Qt.AlignCenter)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.contentLabel, alignment=Qt.AlignCenter)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

        StyleSheet.LINK_CARD.apply(self)