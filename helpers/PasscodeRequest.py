import asyncio
import sys
from functools import wraps

from PyQt5.QtWidgets import QWidget, QApplication

from passcode.passcodewindow import PasscodeWidget


def passcode_setup(f):
    def decorator(*args, **kwargs):
        def onPasscodeEntered(passcode):
            w.destroy()
            f(passcode=passcode, *args, **kwargs)

        w = PasscodeWidget("Enter new passcode", onPasscodeEntered)
        w.show()

    return decorator


def passcode_required(f):
    def decorator(*args, **kwargs):
        def onPasscodeEntered(passcode):
            w.destroy()
            f(passcode=passcode, *args, **kwargs)

        w = PasscodeWidget("Confirmation required", onPasscodeEntered)
        w.show()

    return decorator
