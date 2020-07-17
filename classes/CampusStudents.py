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
        r = self.auth.api_call("students")
        return r

    def get_student(self, pid):
        r = self.auth.api_call(f"students/{pid}")
        return r
