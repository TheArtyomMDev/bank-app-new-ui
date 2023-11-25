import json
import os


class ConfigManager:
    CONFIG_NAME = "config.txt"

    def __init__(self):
        if not os.path.isfile("config.txt"):
            self.__create_config()

    def __create_config(self):
        with open(self.CONFIG_NAME, "w") as f:
            f.write(json.dumps({"logged": False}))

    def __get_config(self):
        with open(self.CONFIG_NAME, "r") as f:
            return json.loads(f.read())

    def is_logged(self):
        return self.__get_config()["logged"]

    def get_token(self):
        return self.__get_config()["token"]

    def set_token(self, token):
        config = self.__get_config()
        config["token"] = token
        config["logged"] = True
        with open(self.CONFIG_NAME, "w") as f:
            f.write(json.dumps(config))
