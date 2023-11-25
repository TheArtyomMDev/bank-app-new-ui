# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel, QSizePolicy

from qfluentwidgets import Pivot, setTheme, Theme, SegmentedWidget, FluentIcon

from gallery.app.common.style_sheet import StyleSheet
from login.screens.Login import LoginWidget

class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet("""
        #     Demo{background: white}
        #     QLabel{
        #         font: 20px 'Segoe UI';
        #         background: rgb(242,242,242);
        #         border-radius: 8px;
        #     }
        # """)
        self.resize(400, 400)

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.songInterface = LoginWidget()
        self.albumInterface = QLabel('Album Interface', self)

        # add items to pivot
        self.addSubInterface(self.songInterface, 'songInterface', 'Login')
        self.addSubInterface(self.albumInterface, 'albumInterface', 'SignUp')

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.songInterface)
        self.pivot.setCurrentItem(self.songInterface.objectName())

        self.setObjectName('view')
        StyleSheet.GALLERY_INTERFACE.apply(self)

    def addSubInterface(self, widget: QWidget, objectName, text):
        widget.setObjectName(objectName)

        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    app.exec_()