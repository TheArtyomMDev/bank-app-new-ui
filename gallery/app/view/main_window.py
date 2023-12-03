# coding: utf-8
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, FluentWindow,
                            SplashScreen)

from helpers.ConfigManager import ConfigManager
from .exchange_input_interface import ExchangeInputInterface
from .gallery_interface import GalleryInterface
from .home_interface import HomeInterface
from .transfer_input_interface import TransferMoneyInputInterface
from ..common.config import cfg
from ..common.signal_bus import signalBus
from ..common.translator import Translator

config = ConfigManager()

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create sub interface
        self.homeInterface = HomeInterface(self)

        self.trasferMoneyInterface = TransferMoneyInputInterface(self)
        self.exchangeMoneyInterface = ExchangeInputInterface(self)

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.trasferMoneyInterface, FIF.SEND, t.transfer, pos)
        self.addSubInterface(self.exchangeMoneyInterface, FIF.SYNC, t.exchange, pos)

        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget(config.get_tag(), ':/gallery/images/shoko.png'),
            position=NavigationItemPosition.BOTTOM
        )
    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowTitle('Banky')

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)
