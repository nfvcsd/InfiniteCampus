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

    def api_call(self, endpoint):
        test = OAuth1Session(self.key, client_secret=self.secret)
        r = test.get(f"{self.url}{endpoint}")
        return r.json()

    def get_student_ids(self):
        data = []
        self.get_credentials()
        r = self.api_call("students")
        for user in r["users"]:
            sourcedid = user["sourcedId"]
            name = f"{user['givenName']} {user['familyName']}"
            if sourcedid[0] == "s":
                sourcedid = f"{sourcedid[1:]}"
            sourcedid = int(sourcedid)
            data.append({"name": name, "ID": f"{sourcedid:04}"})
        return data
