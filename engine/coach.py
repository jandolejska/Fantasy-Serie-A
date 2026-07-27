import json


# =========================
# LOAD COACH GRADES
# =========================

def load_coach_grades(round_number):

    with open(
        f"data/coaches/round{round_number}.json",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# GET COACH GRADE
# =========================

def get_coach_grade(coach_name, round_number):

    grades = load_coach_grades(round_number)

    grade = grades.get(coach_name, 0)

    if isinstance(grade, str):
        grade = grade.replace(",", ".")

    return float(grade)