#!/opt/nfv/bin/python3.8

import os
import json

try:
    from requests_oauthlib import OAuth1Session
except ModuleNotFoundError:
    print("Please install requirements.txt")


class Credentials:
    def __init__(self, name):
        self.name = name
        self.key = ""
        self.secret = ""
        self.url = ""
        self.schools = ""

    def get_credentials(
        self, file=os.path.join(os.path.dirname(__file__), "../config.json")
    ):
        with open(file, "r") as config:
            data = json.load(config)
            for key in data:
                if data[key] == "":
                    print("Please check config file")
            else:
                self.key = data["api_key"]
                self.secret = data["api_secret"]
                self.url = data["base_url"]
                self.schools = data["schools"]

    def api_call(self, endpoint):
        test = OAuth1Session(self.key, client_secret=self.secret)
        r = test.get(f"{self.url}{endpoint}?limit=5000")
        return r.json()

    def get_schools(self):
        return self.schools
