from asyncio import Future

from helpers.PasscodeRequest import passcode_setup


class ServerApi:

    @passcode_setup
    def login(self, email, password, passcode):
        print("Server Here: " + passcode)
