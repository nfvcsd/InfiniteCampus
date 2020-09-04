#!/opt/nfv/bin/python3.8
from classes.CampusStudents import Students
import csv
import os
from datetime import datetime

now = datetime.now()
campus = Students()
filename = f"import_{now}.csv"
file = os.path.join(os.path.dirname(__file__), "hmhsam", f"{filename}")

schools = campus.auth.get_schools()


def main():
    print(schools)
    with open(f"{file}", "w+", newline="") as csvfile:
        fieldnames = [
            "USER_NAME",
            "PASSWORD",
            "SIS_ID",
            "FIRST_NAME",
            "MIDDLE_NAME",
            "LAST_NAME",
            "GRADE",
            "SCHOOL_NAME",
            "CLASS_NAME",
            "LEXILE_SCORE",
            "LEXILE_MOD_DATE",
            "ETHNIC_CAUCASIAN",
            "ETHNIC_AFRICAN_AM",
            "ETHNIC_HISPANIC",
            "ETHNIC_PACIFIC_ISL",
            "ETHNIC_AM_IND_AK_NATIVE",
            "ETHNIC_ASIAN",
            "ETHNIC_TWO_OR_MORE_RACES",
            "GENDER_MALE",
            "GENDER_FEMALE",
            "AYP_ECON_DISADVANTAGED",
            "AYP_LTD_ENGLISH_PROFICIENCY",
            "AYP_GIFTED_TALENTED",
            "AYP_MIGRANT",
            "AYP_WITH_DISABILITIES",
            "EXTERNAL_ID",
            "LAST_COL",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for school in schools:
            students = campus.get_school_students(school)["users"]
            for student in students:
                # print(student)
                sourcedid = student["sourcedId"]
                if sourcedid[0] == "s":
                    sourcedid = f"{sourcedid[1:]}"
                sourcedid = int(sourcedid)
                writer.writerow(
                    {
                        "FIRST_NAME": student["givenName"],
                        "LAST_NAME": student["familyName"],
                        "PASSWORD": sourcedid,
                    }
                )


if __name__ == "__main__":
    main()
