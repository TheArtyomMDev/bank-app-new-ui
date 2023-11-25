import asyncio
import sys
from functools import wraps

from PyQt5.QtWidgets import QWidget, QApplication

from passcode.passcodewindow import PasscodeWidget


def passcode_setup(f):
    # future = asyncio.Future()
    #

    def decorator(*args, **kwargs):
        def onPasscodeEntered(passcode):
            print(passcode)
            return passcode

        # result = await future

        passcode = ""

        async def main():
            w = PasscodeWidget(onPasscodeEntered)
            w.show()

            while True:
                passcode = w.passcode

        asyncio.run(main())

        while len(passcode) != 4:
            pass

        return f(*args, **kwargs)

    return decorator
