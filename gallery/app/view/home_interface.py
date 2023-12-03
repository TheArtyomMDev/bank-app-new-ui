# coding:utf-8
import datetime

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QRectF, QCoreApplication, QThreadPool, QThread, QObject, QRunnable, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QLinearGradient
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidgetItem, QHBoxLayout
from qfluentwidgets import ScrollArea, isDarkTheme, TitleLabel, ListWidget, IndeterminateProgressRing

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
        self.v_box_layout = QVBoxLayout(self)

        self.gallery_label = QLabel(f'Welcome back, {config.get_tag()}!', self)
        self.banner = QPixmap(':/gallery/images/header1.png')
        # self.linkCardView = LinkCardView(self)

        basic_input_view = SampleCardView(
            self.tr("Quick Actions"), self.view)
        basic_input_view.addSampleCard(
            icon=":/gallery/images/controls/Money.png",
            title="Transfer money",
            content=self.tr("Just 2 clicks to get it done!"),
            routeKey="transferInputInterface",
            index=0
        )
        basic_input_view.addSampleCard(
            icon=":/gallery/images/controls/Stats.png",
            title="Exchange rates",
            content=self.tr("Wanna buy those green sheets?"),
            routeKey="exchangeInputInterface",
            index=0
        )

        self.gallery_label.setObjectName('galleryLabel')

        self.v_box_layout.setSpacing(0)
        self.v_box_layout.setContentsMargins(0, 20, 0, 0)
        self.v_box_layout.addWidget(self.gallery_label)
        self.v_box_layout.addWidget(basic_input_view, 1, Qt.AlignBottom)
        self.v_box_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

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
        self.load_widgets()

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

    def load_widgets(self):
        main_v_layout = QVBoxLayout()
        main_v_layout.setContentsMargins(40, 0, 0, 0)

        title = TitleLabel(self.tr('Recent transactions'))
        title.setObjectName("titleLabel")
        title.setMaximumHeight(50)

        title_layout = QHBoxLayout()
        title_layout.addWidget(title)
        self.update_indicator = IndeterminateProgressRing(self)
        self.update_indicator.setFixedSize(50, 50)
        self.update_indicator.setVisible(False)
        title_layout.addWidget(self.update_indicator)

        tmp_widget = QWidget()
        tmp_widget.setLayout(title_layout)
        tmp_widget.setMaximumWidth(500)

        main_v_layout.addWidget(tmp_widget)

        self.transaction_list = ListWidget()
        self.transaction_list.setSpacing(5)

        self.transaction_list.setFixedWidth(500)

        main_v_layout.addWidget(self.transaction_list)

        temp_widget = QWidget()
        temp_widget.setLayout(main_v_layout)

        self.vBoxLayout.addWidget(temp_widget)

        self.updateTransactions()

    def updateTransactionsView(self):
        self.transaction_list.clear()
        transactions = []
        for elem in self.all_trans["sender"]:
            elem["type"] = "sender"
            transactions.append(elem)

        for elem in self.all_trans["receiver"]:
            elem["type"] = "receiver"
            transactions.append(elem)

        transactions.sort(key=lambda x: x["time"], reverse=True)

        for elem in transactions:
            item = QListWidgetItem()
            self.transaction_list.addItem(item)

            if elem["type"] == "sender":
                prefix = "-"
            else:
                prefix = "+"

            date = datetime.datetime.fromtimestamp(elem["time"]).strftime("%Y-%m-%d %H:%M:%S")
            card = TransactionCard(f"{prefix} {elem['amount']}", date, elem["message"])

            self.transaction_list.setItemWidget(item, card)

        self.update_indicator.setVisible(False)

    def updateTransactions(self):
        self.update_indicator.setVisible(True)

        class UpdateTransactions(QObject):
            finished = pyqtSignal()

            def startWork(self2):
                self.all_trans = api.get_transactions()
                self2.finished.emit()

        self.worker = UpdateTransactions()

        self.worker.moveToThread(self.th)

        self.th.started.connect(self.worker.startWork)
        self.worker.finished.connect(self.th.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.updateTransactionsView)

        self.th.start()

    def showEvent(self, a0: QtGui.QShowEvent):
        self.updateTransactions()
