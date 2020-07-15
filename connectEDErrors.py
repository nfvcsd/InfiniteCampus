#!/opt/nfv/bin/python3.8
import csv
import json
import sys

try:
    from requests_oauthlib import OAuth1Session
except ModuleNotFoundError:
    print("Please install requirements.txt")


def get_credentials(file="config.json"):
    with open(file, "r") as config:
        data = json.load(config)
        for key in data:
            if data[key] == "":
                print("Please check config file")
        else:
            return data["api_key"], data["api_secret"], data["base_url"]


def api_call(key, secret, url):
    test = OAuth1Session(key, client_secret=secret,)
    r = test.get(url)
    return r.json()


def check_error(error):
    # put code here to read a single csv line and check for error info
    print("filler text")


def main():
    # Give me some Main
    (key, secret, base_url) = get_credentials()

    data = api_call(key, secret, f"{base_url}schools?limit=50000")
    print(data)


if __name__ == "__main__":
    main()
