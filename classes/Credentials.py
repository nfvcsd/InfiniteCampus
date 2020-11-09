#!/opt/nfv/bin/python3.8

import os
import json
import logging

try:
    from requests_oauthlib import OAuth1Session
except ModuleNotFoundError:
    print("Please install requirements.txt")

# LOGGING
logger = logging.getLogger("Credentials")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
ch.setFormatter(formatter)
logger.addHandler(ch)


class Credentials:
    def __init__(self, name):
        self.name = name
        self.key = ""
        self.secret = ""
        self.url = ""
        self.sam_schools = ""
        self.class_matches = ""
        self.destiny_schools = ""
        self.destiny_school_mapping = ""

    def get_credentials(
        self, file=os.path.join(os.path.dirname(__file__), "../config.json")
    ):
        logger.info("Checking For Credentials")
        with open(file, "r") as config:
            data = json.load(config)
            ###### THIS SHOULDN'T WORK SHOULD IT? A FOR ELSE LOOP?
            for key in data:
                if data[key] == "":
                    logger.warning(f"{key} is missing a value")
            else:
                self.key = data["api_key"]
                self.secret = data["api_secret"]
                self.url = data["base_url"]
                self.sam_schools = data["SAMSchools"]
                self.destiny_schools = data["DestinySchools"]
                self.class_matches = data["class_matches"]
                self.destiny_school_mapping = data["Destiny_School_Map"]
                logger.info("Credentials Set")

    def api_call(self, endpoint):
        test = OAuth1Session(self.key, client_secret=self.secret)
        r = test.get(f"{self.url}{endpoint}?limit=5000")
        if r.status_code != 200:
            logger.error("API Call returned non 200 status")
        return r.json()

    def get_sam_schools(self):
        return self.schools

    def get_destiny_schools(self):
        return self.destiny_schools

    def get_classes(self):
        return self.class_matches

    def get_destiny_school_mapping(self):
        """Returns the school mapping from the config file"""
        return self.destiny_school_mapping
