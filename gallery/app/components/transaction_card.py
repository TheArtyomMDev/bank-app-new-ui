from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QFrame, QHBoxLayout, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets.components.widgets.flyout import Flyout

from gallery.app.common.style_sheet import StyleSheet


class TransactionCard(QFrame):

    def __init__(self, amount, sender, message, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(60)
        # self.iconWidget = IconWidget(icon, self)
        self.amountLabel = QLabel(amount, self)
        self.senderLabel = QLabel(sender, self)
        # self.urlWidget = IconWidget(FluentIcon.LINK, self)

        self.message = message
        self.__initWidget()

    def __initWidget(self):
        self.setCursor(Qt.PointingHandCursor)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(24, 0, 24, 0)
        self.hBoxLayout.addWidget(self.amountLabel)
        self.hBoxLayout.addStretch()
        self.hBoxLayout.addWidget(self.senderLabel)
        self.hBoxLayout.addSpacing(2)

        self.amountLabel.setObjectName('titleLabel')
        self.senderLabel.setObjectName('titleLabel')

        self.view = QWidget(self)

        StyleSheet.TRANSACTION_CARD.apply(self)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        super().mouseReleaseEvent(a0)
        self.show_flyout()

    def show_flyout(self):
        Flyout.create(
            icon=FIF.MESSAGE,
            title='Message:',
            content=self.message,
            target=self.view,
            parent=self.view
        )
