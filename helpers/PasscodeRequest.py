import asyncio
import sys
from functools import wraps

from PyQt5.QtWidgets import QWidget, QApplication

from passcode.passcodewindow import PasscodeWidget


def passcode_setup(f):
    def decorator(*args, **kwargs):
        def onPasscodeEntered(passcode):
            w.destroy()
            print("Here: " + passcode)
            f(passcode=passcode, *args, **kwargs)

        w = PasscodeWidget(onPasscodeEntered)
        w.show()

    return decorator
