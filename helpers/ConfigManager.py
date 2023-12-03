import json
import os


class ConfigManager:
    CONFIG_NAME = "config.json"

    def __init__(self):
        if not os.path.isfile(self.CONFIG_NAME):
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

    def get_tag(self):
        return self.__get_config()["tag"]

    def __add_field(self, name, param):
        config = self.__get_config()
        config[name] = param
        with open(self.CONFIG_NAME, "w") as f:
            f.write(json.dumps(config))

    def set_token(self, token):
        self.__add_field("token", token)
        self.__add_field("logged", True)

    def set_tag(self, tag):
        self.__add_field("tag", tag)

    def logout(self):
        self.__add_field("logged", False)
