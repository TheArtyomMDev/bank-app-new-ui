from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

import ctypes
from ctypes.wintypes import DWORD, HRGN, HWND, BOOL, LPVOID, PINT, ULONG
from ctypes import windll, c_bool, c_int, POINTER, Structure


class AccentPolicy(Structure):
    _fields_ = [
        ('AccentState', DWORD),
        ('AccentFlags', DWORD),
        ('GradientColor', DWORD),
        ('AnimationId', DWORD),
    ]


# SOURCE: http://undoc.airesoft.co.uk/user32.dll/GetWindowCompositionAttribute.php
class WINCOMPATTRDATA(Structure):
    _fields_ = [
        ('Attribute', DWORD),
        ('Data', POINTER(AccentPolicy)),
        ('SizeOfData', ULONG),
    ]


# SOURCE: http://undoc.airesoft.co.uk/user32.dll/SetWindowCompositionAttribute.php
# BOOL WINAPI SetWindowCompositionAttribute (
#     HWND hwnd,
#     WINCOMPATTRDATA* pAttrData
# )
SetWindowCompositionAttribute = windll.user32.SetWindowCompositionAttribute
SetWindowCompositionAttribute.restype = c_bool
SetWindowCompositionAttribute.argtypes = [c_int, POINTER(WINCOMPATTRDATA)]


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)

        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)

        # SOURCE: http://howtucode.com/c-pinvoke-user32dll-getwindowcompositionattribute-13192.html
        accent_policy = AccentPolicy()
        accent_policy.AccentState = 3  # ACCENT_ENABLE_BLURBEHIND;

        win_comp_attr_data = WINCOMPATTRDATA()
        win_comp_attr_data.Attribute = 19  # WCA_ACCENT_POLICY
        win_comp_attr_data.SizeOfData = ctypes.sizeof(accent_policy)
        win_comp_attr_data.Data = ctypes.pointer(accent_policy)

        hwnd = c_int(self.winId())
        ok = SetWindowCompositionAttribute(hwnd, ctypes.pointer(win_comp_attr_data))
        print(ok)

        print(ctypes.get_last_error())

        self.old_pos = None
        self.frame_color = Qt.darkCyan

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(QPushButton("Закрыть окно", clicked=self.close))

        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None

    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return

        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)


if __name__ == '__main__':
    app = QApplication([])

    w = Widget()
    w.resize(400, 300)
    # w.show()

    lay = QVBoxLayout()
    lay.addWidget(QLabel("dd"))
    lay.addWidget(w)

    bas = QWidget()
    bas.resize(300, 300)
    bas.setLayout(lay)
    bas.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 white, stop: 0.4 gray, stop:1 green)")
    bas.show()

    w2 = Widget()
    w2.resize(400, 300)
    w2.show()

    app.exec()