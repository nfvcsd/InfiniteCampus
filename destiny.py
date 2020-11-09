#!/opt/nfv/bin/python3.8
from classes.CampusStudents import Students
from classes.CampusTeachers import Teachers
import csv
import os
from datetime import datetime
import logging
import typing

# NFE, NFVHS, nfvms/vall, WUE
now = datetime.now()
campus = Students()
errors = {}

logname = f"{now}.log"
loglocation = os.path.join(os.path.dirname(__file__), "destiny", f"{logname}")

teachers = Teachers()
schools = campus.auth.get_destiny_schools()
school_map = campus.auth.get_destiny_school_mapping()
# LOGGING SETUP
logger = logging.getLogger("DESTINY")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
fh = logging.FileHandler(loglocation)
fh.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


def student_csv():
    logger.info("Starting student CSV Generation")
    filename = f"student_import_{now}.csv"
    file = os.path.join(os.path.dirname(__file__), "destiny", f"{filename}")
    logger.debug(f"File Location: {file}")
    with open(f"{file}", "w+", newline="") as csvfile:
        fieldnames = [
            "field_siteShortName",
            "field_barcode",
            "field_districtID",
            "field_lastName",
            "field_firstName",
            "field_middleName",
            "field_nickname",
            "field_patronType",
            "field_accessLevel",
            "field_resourceGroup",
            "field_status",
            "field_gender",
            "field_homeroom",
            "field_gradeLevel",
            "field_cardExpires",
            "field_isAcceptableUsePolicyOnFile",
            "field_isTeacher",
            "field_userDefined1",
            "field_userDefined2",
            "field_userDefined3",
            "field_userDefined4",
            "field_userDefined5",
            "field_graduationYear",
            "field_birthdate",
            "field_username",
            "field_password",
            "field_emailPrimary",
            "field_emailSecondary",
            "field_email3",
            "field_email4",
            "field_email5",
            "field_addressPrimaryLine1",
            "field_addressPrimaryLine2",
            "field_addressPrimaryCity",
            "field_addressPrimaryState",
            "field_addressPrimaryZipCode",
            "field_addressPrimaryPhoneNumberPrimary",
            "field_addressPrimaryPhoneNumberSecondary",
            "field_addressSecondaryLine1",
            "field_addressSecondaryLine2",
            "field_addressSecondaryCity",
            "field_addressSecondaryState",
            "field_addressSecondaryZipCode",
            "field_addressSecondaryPhoneNumberPrimary",
            "field_addressSecondaryPhoneNumberSecondary",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for school in schools:
            school_name = campus.get_school(school)["org"]["name"]
            if school_name in school_map:
                school_name = school_map[school_name]
            else:
                logger.warn(f"{school_name} not in school mapping")
            logger.info(f"Starting School {school_name}")
            students = campus.get_school_students(school)["users"]
            for student in students:
                fname = student["givenName"]
                lname = student["familyName"]
                logger.info(f"Processing {fname} {lname}")
                sourcedid = student["sourcedId"]
                if sourcedid[0] == "s":
                    sourcedid = f"{sourcedid[1:]}"
                sourcedid = int(sourcedid)
                # password = f"{(student['givenName'][:1]).upper()}{(student['familyName'][:1]).lower()}{sourcedid:06}"
                password = sourcedid
                grade = student["grades"][0]
                username = student["username"]
                graduation_year = f"20{username[:2]}"
                try:
                    graduation_year = int(graduation_year)
                except ValueError:
                    errors[f"{fname} {lname}"] = "Graduation Year"
                    logger.warning(
                        f"Student {fname} {lname} does not have a user account starting with their graduation year!"
                    )
                    graduation_year = int(0000)
                if grade[0] == "0":
                    grade = grade[1:]
                try:
                    middleName = student["middleName"]
                except KeyError:
                    middleName = ""
                    logger.debug(f"No middle name for {fname} {lname}")
                writer.writerow(
                    {
                        "field_firstName": student["givenName"],
                        "field_lastName": student["familyName"],
                        "field_password": password,
                        "field_username": student["username"],
                        "field_middleName": middleName,
                        "field_barcode": f"P {sourcedid}",
                        "field_districtID": sourcedid,
                        "field_gradeLevel": grade,
                        "field_siteShortName": school_name,
                        "field_patronType": "Student",
                        "field_status": "A",
                        "field_isTeacher": "F",
                        "field_emailPrimary": student["email"],
                        "field_graduationYear": graduation_year,
                    }
                )


def main():
    student_csv()


if __name__ == "__main__":
    main()
