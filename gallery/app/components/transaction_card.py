from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout
from qfluentwidgets import TextWrap, FluentIcon
from qfluentwidgets.components.widgets.flyout import IconWidget

from gallery.app.common.style_sheet import StyleSheet


class TransactionCard(QFrame):

    def __init__(self, amount, sender, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(120)
        # self.iconWidget = IconWidget(icon, self)
        self.amountLabel = QLabel(amount, self)
        self.senderLabel = QLabel(sender, self)
        # self.urlWidget = IconWidget(FluentIcon.LINK, self)

        self.__initWidget()

    def __initWidget(self):
        self.setCursor(Qt.PointingHandCursor)

        # self.iconWidget.setFixedSize(54, 54)
        # self.urlWidget.setFixedSize(16, 16)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(24, 24, 24, 24)
        # self.vBoxLayout.addWidget(self.iconWidget)
        # self.vBoxLayout.addSpacing(16)
        self.hBoxLayout.addWidget(self.amountLabel)
        self.hBoxLayout.addStretch()
        self.hBoxLayout.addWidget(self.senderLabel)
        self.hBoxLayout.addSpacing(2)
        # self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        # self.urlWidget.move(170, 192)

        self.amountLabel.setObjectName('titleLabel')
        self.senderLabel.setObjectName('titleLabel')

        StyleSheet.TRANSACTION_CARD.apply(self)