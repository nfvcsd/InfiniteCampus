#!/opt/nfv/bin/python3.8
from .Credentials import Credentials


class Students:
    def __init__(self):
        self.auth = Credentials("students")
        self.auth.get_credentials()

    def get_student_ids(self):
        data = []
        r = self.auth.api_call("students")
        for user in r["users"]:
            sourcedid = user["sourcedId"]
            name = f"{user['givenName']} {user['familyName']}"
            if sourcedid[0] == "s":
                sourcedid = f"{sourcedid[1:]}"
            sourcedid = int(sourcedid)
            data.append({"name": name, "ID": f"{sourcedid:04}"})
        return data

    def get_students(self):
        r = self.auth.api_call("rostering/v1p2/students")
        return r

    def get_student(self, pid):
        r = self.auth.api_call(f"rostering/v1p2/students/{pid}")
        return r

    def get_schools(self):
        r = self.auth.api_call("rostering/v1p2/schools")
        return r

    def get_school(self, pid):
        r = self.auth.api_call(f"rostering/v1p2/schools/{pid}")
        return r

    def get_school_students(self, pid):
        r = self.auth.api_call(f"rostering/v1p2/schools/{pid}/students")
        return r

    def get_student_classes(self, pid):
        r = self.auth.api_call(f"rostering/v1p2/students/{pid}/classes")
        return r

    def get_class(self, sourcedId):
        r = self.auth.api_call(f"rostering/v1p2/classes/{sourcedId}")
        return r
