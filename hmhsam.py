#!/opt/nfv/bin/python3.8
from classes.CampusStudents import Students
from classes.CampusTeachers import Teachers
import csv
import os
from datetime import datetime
import logging

now = datetime.now()
campus = Students()


logname = f"{now}.log"
loglocation = os.path.join(os.path.dirname(__file__), "hmhsam", f"{logname}")

teachers = Teachers()
schools = campus.auth.get_schools()
class_matches = campus.auth.get_classes()
class_sourcedids = []
# LOGGING SETUP
logger = logging.getLogger("SAM")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
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
    file = os.path.join(os.path.dirname(__file__), "hmhsam", f"{filename}")
    logger.debug(f"File Location: {file}")
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
            school_name = campus.get_school(school)["org"]["name"]
            logger.info(f"Starting School {school_name}")
            students = campus.get_school_students(school)["users"]
            for student in students:
                fname = student["givenName"]
                lname = student["familyName"]
                logger.info(f"Processing {fname} {lname}")
                sourcedid = student["sourcedId"]
                student_classes = campus.get_student_classes(sourcedid)[
                    "classes"
                ]
                grade = student["grades"][0]
                if grade[0] == "0":
                    grade = grade[1:]
                for student_class in student_classes:
                    for match in class_matches:
                        if match in student_class["title"]:
                            if (
                                student_class["sourcedId"]
                                not in class_sourcedids
                            ):
                                class_sourcedids.append(
                                    student_class["sourcedId"]
                                )
                            classname = f"{school_name} {grade}"
                            break
                if sourcedid[0] == "s":
                    sourcedid = f"{sourcedid[1:]}"
                sourcedid = int(sourcedid)
                password = f"{(student['givenName'][:1]).upper()}{(student['familyName'][:1]).lower()}{sourcedid:06}"
                try:
                    middleName = student["middleName"]
                except KeyError:
                    middleName = ""
                    logger.debug(f"No middle name for {fname} {lname}")
                writer.writerow(
                    {
                        "FIRST_NAME": student["givenName"],
                        "LAST_NAME": student["familyName"],
                        "PASSWORD": password,
                        "USER_NAME": student["username"],
                        "MIDDLE_NAME": middleName,
                        "SIS_ID": sourcedid,
                        "GRADE": grade,
                        "SCHOOL_NAME": school_name,
                        "CLASS_NAME": classname,
                    }
                )
    logger.info("CSV Complete")


def teacher_csv():
    logger.info("Starting Teacher CSV Generation")
    filename = f"teacher_import_{now}.csv"
    file = os.path.join(os.path.dirname(__file__), "hmhsam", f"{filename}")
    logger.debug(f"File Location: {file}")
    with open(f"{file}", "w+", newline="") as csvfile:
        fieldnames = [
            "DISTRICT_USER_ID",
            "SPS_ID",
            "PREFIX",
            "FIRST_NAME",
            "LAST_NAME",
            "TITLE",
            "SUFFIX",
            "EMAIL",
            "USER_NAME",
            "PASSWORD",
            "SCHOOL_NAME",
            "CLASS_NAME",
            "EXTERNAL_ID",
            "LAST_COL",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for class_sourcedid in class_sourcedids:
            # logger.info("Trying to get data for class: {class_sourcedid}")
            class_data = teachers.get_class_teacher(class_sourcedid)
            course_data = campus.get_class(class_sourcedid)
            school_name = campus.get_school(
                course_data["class"]["school"]["sourcedId"]
            )["org"]["name"]
            class_grade = int(course_data["class"]["title"][0])
            class_name = f"{school_name} {class_grade:02}"
            sourcedid = class_data["sourcedId"]
            if sourcedid[0] == "t":
                sourcedid = f"{sourcedid[1:]}"
            sourcedid = int(sourcedid)
            password = f"{(class_data['givenName'][:1]).upper()}{(class_data['familyName'][:1]).lower()}{sourcedid:06}"
            # logger.info(class_data)
            writer.writerow(
                {
                    "DISTRICT_USER_ID": class_data["sourcedId"],
                    "FIRST_NAME": class_data["givenName"],
                    "LAST_NAME": class_data["familyName"],
                    "EMAIL": class_data["email"],
                    "USER_NAME": class_data["username"],
                    "PASSWORD": password,
                    "SCHOOL_NAME": school_name,
                    "CLASS_NAME": class_name,
                }
            )


def main():
    student_csv()
    teacher_csv()


if __name__ == "__main__":
    main()
