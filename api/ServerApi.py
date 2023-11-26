from asyncio import Future

import requests

from helpers.ConfigManager import ConfigManager
from helpers.PasscodeRequest import passcode_setup, passcode_required

config = ConfigManager()

class ServerApi:
    SERVER_URL = "http://localhost:5000"
    auth_token = None

    def __init__(self):
        self.access_token = None
        self.refresh_token = None

        if config.is_logged():
            self.__set_token(config.get_token())

    @passcode_required
    def transfer(self, receiver, amount, message, onFinished, passcode):
        res = self.exec_request("/transfer_money", "POST", {
            "receiver": receiver,
            "amount": amount,
            "message": message
        }, passcode=passcode)

        onFinished(res)

    def get_balance(self):
        res = self.exec_request("/get_balance", "GET")
        # print(res)
        return res["data"]["balance"]

    def get_tag(self):
        res = self.exec_request("/tag", "GET")
        # print(res)
        return res["data"]

    def get_transactions(self):
        res = self.exec_request("/transactions", "GET")
        print(res)
        return res["data"]

    def get_users(self):
        res = self.exec_request("/search_users", "POST", {})
        # print(res)
        return res["data"]["users"]

    @passcode_setup
    def login(self, email, password, onLogged, onFailed, passcode):
        res = self.exec_request("/signin", "POST", {
            "email": email,
            "password": password,
            "passcode": passcode
        })

        print(res)

        if res["status"] == "OK":
            self.refresh_token = res["data"]["refresh_token"]
            self.access_token = res["data"]["access_token"]
            onLogged(self.refresh_token)
        else:
            onFailed(res["reason"])

    def __set_token(self, token):
        self.refresh_token = token

        res = self.exec_request("/access_token", "POST", {
            "token": token
        })

        self.access_token = res["data"]["access_token"]

    def exec_request(self, path, method, body=None, passcode=None):
        headers = {}

        if self.access_token is not None:
            headers["Authorization"] = self.access_token

        if passcode is not None:
            headers["Passcode"] = passcode

        return requests.request(method, self.SERVER_URL + path, headers=headers, json=body).json()
