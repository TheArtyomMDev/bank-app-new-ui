# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """ Signal bus """

    switch_to_sample_card = pyqtSignal(str, int)
    mica_enable_changed = pyqtSignal(bool)
    support_signal = pyqtSignal()


signal_bus = SignalBus()