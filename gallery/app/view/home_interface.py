# coding:utf-8
import datetime

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QRectF, QCoreApplication, QThreadPool, QThread, QObject, QRunnable, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QLinearGradient
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidgetItem
from qfluentwidgets import ScrollArea, isDarkTheme, TitleLabel, ListWidget

from helpers import InstanceHolders
from helpers.ConfigManager import ConfigManager
from ..common.style_sheet import StyleSheet
from ..components.sample_card import SampleCardView
from ..components.transaction_card import TransactionCard

api = InstanceHolders.api

config = ConfigManager()


class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.galleryLabel = QLabel(f'Welcome back, {config.get_tag()}!', self)
        self.banner = QPixmap(':/gallery/images/header1.png')
        # self.linkCardView = LinkCardView(self)

        basicInputView = SampleCardView(
            self.tr("Quick Actions"), self.view)
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Money.png",
            title="Transfer money",
            content=self.tr("Just 2 clicks to get it done!"),
            routeKey="transferInputInterface",
            index=0
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Stats.png",
            title="Exchange rates",
            content=self.tr("Wanna buy those green sheets?"),
            routeKey="exchangeInputInterface",
            index=0
        )

        self.galleryLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(basicInputView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # init linear gradient effect
        gradient = QLinearGradient(0, 0, 0, h)

        # draw background color
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))

        painter.fillPath(path, QBrush(gradient))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), transformMode=Qt.SmoothTransformation)
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    """ Home interface """
    all_trans = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.th = QThread()
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 0, 0, 0)

        title = TitleLabel(self.tr('Recent transactions'))
        title.setObjectName("titleLabel")
        title.setMaximumHeight(50)
        main_layout.addWidget(title)

        self.transactionList = ListWidget()
        self.transactionList.setSpacing(5)

        # all_trans = api.get_transactions()
        #
        # transactions = []
        # for elem in all_trans["sender"]:
        #     elem["type"] = "sender"
        #     transactions.append(elem)
        #
        # for elem in all_trans["receiver"]:
        #     elem["type"] = "receiver"
        #     transactions.append(elem)
        #
        # for elem in transactions:
        #     item = QListWidgetItem()
        #     self.transactionList.addItem(item)
        #
        #     if elem["type"] == "sender":
        #         prefix = "-"
        #     else:
        #         prefix = "+"
        #
        #     date = datetime.datetime.fromtimestamp(elem["time"]).strftime("%Y-%m-%d %H:%M:%S")
        #     card = TransactionCard(f"{prefix} {elem['amount']}", date, elem["message"])
        #
        #     self.transactionList.setItemWidget(item, card)

        # self.transactionList.setContentsMargins(40, 40, 40, 40)
        self.transactionList.setFixedWidth(500)

        main_layout.addWidget(self.transactionList)

        temp_widget = QWidget()
        temp_widget.setLayout(main_layout)

        self.vBoxLayout.addWidget(temp_widget)

        self.updateTransactions()

    # def updateTransactionsView(self):
    #     self.transactionList.clear()
    #     transactions = []
    #     for elem in self.all_trans["sender"]:
    #         elem["type"] = "sender"
    #         transactions.append(elem)
    #
    #     for elem in self.all_trans["receiver"]:
    #         elem["type"] = "receiver"
    #         transactions.append(elem)
    #
    #     for elem in transactions:
    #         item = QListWidgetItem()
    #         self.transactionList.addItem(item)
    #
    #         if elem["type"] == "sender":
    #             prefix = "-"
    #         else:
    #             prefix = "+"
    #
    #         date = datetime.datetime.fromtimestamp(elem["time"]).strftime("%Y-%m-%d %H:%M:%S")
    #         card = TransactionCard(f"{prefix} {elem['amount']}", date, elem["message"])
    #
    #         self.transactionList.setItemWidget(item, card)

    def updateTransactionsView(self):
        if self.transactionList is None:
            return

        print("Callback")
        self.transactionList.clear()
        print(self.all_trans)

        transactions = []
        for elem in self.all_trans["sender"]:
            elem["type"] = "sender"
            transactions.append(elem)

        for elem in self.all_trans["receiver"]:
            elem["type"] = "receiver"
            transactions.append(elem)

        for elem in transactions:
            item = QListWidgetItem()
            self.transactionList.addItem(item)

            if elem["type"] == "sender":
                prefix = "-"
            else:
                prefix = "+"

            date = datetime.datetime.fromtimestamp(elem["time"]).strftime("%Y-%m-%d %H:%M:%S")
            card = TransactionCard(f"{prefix} {elem['amount']}", date, elem["message"])

            self.transactionList.setItemWidget(item, card)

    def updateTransactions(self):
        print("Update transactions: ")

        class UpdateTransactions(QObject):
            finished = pyqtSignal()

            def startWork(self2):
                self.all_trans = api.get_transactions()
                self2.finished.emit()

        # if self.th is not None:
        #     self.th.quit()
        #     self.th.wait()

        self.worker = UpdateTransactions()


        self.worker.moveToThread(self.th)

        self.th.started.connect(self.worker.startWork)
        self.worker.finished.connect(self.th.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        # self.th.finished.connect(self.th.deleteLater)
        self.worker.finished.connect(self.updateTransactionsView)

        self.th.start()

    def showEvent(self, a0: QtGui.QShowEvent):
        self.updateTransactions()
