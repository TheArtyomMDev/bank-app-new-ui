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

        self.setFixedSize(120, 180)
        self.icon_widget = IconWidget(icon, self)
        self.title_label = QLabel(title, self)
        self.content_label = QLabel(TextWrap.wrap(content, 28, False)[0], self)

        self.__initWidget()
        self.view = QWidget(self)

    def __initWidget(self):
        self.setCursor(Qt.PointingHandCursor)

        self.icon_widget.setFixedSize(100, 100)

        self.v_box_layout = QVBoxLayout(self)
        self.v_box_layout.setSpacing(0)
        self.v_box_layout.addWidget(self.icon_widget, alignment=Qt.AlignCenter)
        self.v_box_layout.addSpacing(16)
        self.v_box_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        self.v_box_layout.addSpacing(8)
        self.v_box_layout.addWidget(self.content_label, alignment=Qt.AlignCenter)

        self.title_label.setObjectName('titleLabel')
        self.content_label.setObjectName('contentLabel')

        StyleSheet.LINK_CARD.apply(self)