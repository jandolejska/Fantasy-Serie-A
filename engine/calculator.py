# =========================
# GRADE
# =========================

def grade_to_float(grade):

    if grade is None:
        return 0.0

    grade = str(grade).replace(",", ".")

    return float(grade)


# =========================
# TEAM SCORE
# =========================

def calculate_team_score(team, home=False, coach_bonus=0):

    total = 0

    for player in team:

        total += grade_to_float(player["grade"])

    if home:
        total += 2

    total += coach_bonus

    return total


# =========================
# SCORE -> GOALS
# =========================

def score_to_goals(score):

    if score <= 65.0:
        return 0
    elif score <= 68.0:
        return 1
    elif score <= 70.5:
        return 2
    elif score <= 73.0:
        return 3
    elif score <= 75.0:
        return 4
    elif score <= 77.0:
        return 5
    elif score <= 78.5:
        return 6
    elif score <= 80.0:
        return 7
    elif score <= 81.5:
        return 8
    elif score <= 83.0:
        return 9
    else:
        return 10