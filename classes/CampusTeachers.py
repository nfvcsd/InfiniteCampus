from .Credentials import Credentials


class Teachers:
    def __init__(self):
        self.auth = Credentials("students")
        self.auth.get_credentials()

    def get_teachers(self):
        r = self.auth.api_call("teachers")
        return r

    def get_teacher(self, pid):
        r = self.auth.api_call(f"teachers/{pid}")
        return r

    def get_teacher_ids(self):
        data = []
        r = self.get_teachers()
        for user in r["users"]:
            sourcedid = user["sourcedId"]
            name = f"{user['givenName']} {user['familyName']}"
            if sourcedid[0] == "s":
                sourcedid = f"{sourcedid[1:]}"
            sourcedid = int(sourcedid)
            data.append({"name": name, "ID": f"{sourcedid:04}"})
        return data
