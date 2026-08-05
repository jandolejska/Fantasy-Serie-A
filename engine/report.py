import json
import os

from engine.results import load_round
from engine.standings import get_ranking
from engine.report_memory import get_template


# =========================
# MANAGER NAME (CASE)
# =========================

# =========================
# MANAGER NAME FORMS
# =========================

MANAGER_FORMS = {

    "Johnny": {
        "nom": "Johnny",
        "acc": "Johnnyho",
        "dat": "Johnnymu",
        "ins": "Johnnym"
    },

    "Goran": {
        "nom": "Goran",
        "acc": "Gorana",
        "dat": "Goranovi",
        "ins": "Goranem"
    },

    "Kuba": {
        "nom": "Kuba",
        "acc": "Kubu",
        "dat": "Kubovi",
        "ins": "Kubou"
    },

    "Matěj": {
        "nom": "Matěj",
        "acc": "Matěje",
        "dat": "Matějovi",
        "ins": "Matějem"
    },

    "Matej": {
        "nom": "Matěj",
        "acc": "Matěje",
        "dat": "Matějovi",
        "ins": "Matějem"
    },

    "Paulie": {
        "nom": "Paulie",
        "acc": "Paulieho",
        "dat": "Pauliemu",
        "ins": "Pau­liem"
    },

    "Francesco": {
        "nom": "Francesco",
        "acc": "Francesca",
        "dat": "Francescovi",
        "ins": "Francescem"
    }

}


def manager_case(name, case="nom"):

    forms = MANAGER_FORMS.get(name)

    if not forms:
        return name

    return forms.get(case, forms["nom"])


# =========================
# CREATE REPORTS FOLDER
# =========================

def create_reports_folder():

    os.makedirs("reports", exist_ok=True)


# =========================
# SAVE REPORT
# =========================

def save_report(round_number, report):

    create_reports_folder()

    with open(
        f"reports/round{round_number}.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================
# LOAD REPORT
# =========================

def load_report(round_number):

    file = f"reports/round{round_number}.json"

    if not os.path.exists(file):
        return None

    with open(
        file,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# GENERATE REPORT
# =========================

def generate_round_report(round_number):

    round_data = load_round(round_number)

    if not round_data:
        return None

    sections = [
        generate_summary(round_data),
        generate_player_section(round_data),
        generate_manager_section(round_data),
        generate_leader_section(round_data),
        generate_special_event(round_data)
    ]

    report = {
        "round": round_number,
        "headline": generate_headline(round_data),
        "sections": [s for s in sections if s],
        "player": round_data["awards"]["player_of_round"]
    }

    save_report(
        round_number,
        report         
    )

    return report


# =========================
# GENERATE HEADLINE
# =========================

def generate_headline(round_data):

    events = []

    total_goals = 0

    best_match = None
    biggest_difference = -1

    for match in round_data["matches"]:

        total_goals += (
            match["home_goals"] +
            match["away_goals"]
        )

        difference = abs(
            match["home_goals"] -
            match["away_goals"]
        )

        if difference > biggest_difference:
            biggest_difference = difference
            best_match = match

    # =====================
    # Nový lídr soutěže
    # =====================

    ranking = get_ranking(round_data["table"])

    previous = load_round(round_data["round"] - 1)

    if ranking and previous:

        previous_ranking = get_ranking(previous["table"])

        if previous_ranking:

            if ranking[0][0] != previous_ranking[0][0]:

                events.append({
                    "priority": 100,
                    "headline": get_template(
                        "LEADER_CHANGE",
                        manager=manager_case(ranking[0][0]),
                        manager_dat=manager_case(ranking[0][0], "dat"),
                        round=round_data["round"]
                    )
                })

    # =====================
    # Samé remízy
    # =====================

    if biggest_difference == 0:

        events.append({
            "priority": 90,
            "headline":
                f"{round_data['round']}. kolo skončilo bez jediného vítěze."
        })

    # =====================
    # Gólová přestřelka
    # =====================

    elif total_goals >= 10:

        events.append({
            "priority": 70,
            "headline":
                f"Ve {round_data['round']}. kole padlo celkem {total_goals} branek."
        })

    # =====================
    # Defenzivní kolo
    # =====================

    elif total_goals <= 4:

        events.append({
            "priority": 60,
            "headline":
                f"Obrany měly navrch. Ve {round_data['round']}. kole padly pouze {total_goals} branky."
        })

    # =====================
    # Nejvyšší výhra
    # =====================

    else:

        if best_match["home_goals"] > best_match["away_goals"]:

            winner = manager_case(best_match["home"])
            loser_acc = manager_case(best_match["away"], "acc")
            loser_dat = manager_case(best_match["away"], "dat")
            loser_ins = manager_case(best_match["away"], "ins")
            goals = (
                f"{best_match['home_goals']}:"
                f"{best_match['away_goals']}"
            )

        else:

            winner = manager_case(best_match["away"])
            loser_acc = manager_case(best_match["home"], "acc")
            loser_dat = manager_case(best_match["home"], "dat")
            loser_ins = manager_case(best_match["home"], "ins")
            goals = (
                f"{best_match['away_goals']}:"
                f"{best_match['home_goals']}"
            )

        events.append({
            "priority": 50,
            "headline": get_template(
                "BIGGEST_WIN",
                winner=winner,
                loser_acc=loser_acc,
                loser_dat=loser_dat,
                loser_ins=loser_ins,
                score=goals,
                round=round_data["round"]
            )
        })

    # =====================
    # Výběr nejlepší zprávy
    # =====================

    events.sort(
        key=lambda e: e["priority"],
        reverse=True
    )

    return events[0]["headline"]

# =========================
# GENERATE SUMMARY
# =========================

def generate_summary(round_data):

    total_goals = 0
    matches = len(round_data["matches"])

    best_match = None
    biggest_difference = -1

    for match in round_data["matches"]:

        total_goals += (
            match["home_goals"] +
            match["away_goals"]
        )

        difference = abs(
            match["home_goals"] -
            match["away_goals"]
        )

        if difference > biggest_difference:
            biggest_difference = difference
            best_match = match

    average = round(total_goals / matches, 2)

    summary = []

    summary.append(
        get_template(
            "SUMMARY_INTRO",
            round=round_data["round"],
            matches=matches,
            goals=total_goals
        )
    )

    if average >= 4:

        summary.append(
            get_template("SUMMARY_ATTACK")
        )

    elif average >= 2.5:

        summary.append(
            get_template("SUMMARY_BALANCED")
        )

    else:

        summary.append(
            get_template("SUMMARY_DEFENSE")
        )

    if biggest_difference == 0:

        summary.append(
            "🤝 Všechna utkání tohoto kola skončila remízou."
        )

    return summary


# =========================
# GENERATE PLAYER SECTION
# =========================

def generate_player_section(round_data):

    player = round_data["awards"]["player_of_round"]

    return get_template(
        "PLAYER_OF_ROUND",
        player=player["name"],
        team=player["team"],
        grade=player["grade"]
    )


# =========================
# GENERATE MANAGER SECTION
# =========================

def generate_manager_section(round_data):

    manager = round_data["awards"]["manager_of_round"]

    return get_template(
        "MANAGER_OF_ROUND",
        manager=manager_case(manager["manager"]),
        score=manager["score"]
    )


# =========================
# GENERATE LEADER SECTION
# =========================

def generate_leader_section(round_data):

    ranking = get_ranking(round_data["table"])

    if not ranking:
        return None

    leader_name = ranking[0][0]

    previous = load_round(round_data["round"] - 1)

    if previous is None:

        return get_template(
            "LEADER_CHANGE",
            manager=manager_case(leader_name),
            manager_dat=manager_case(leader_name, "dat"),
            round=round_data["round"]
        )

    previous_ranking = get_ranking(previous["table"])

    previous_leader = previous_ranking[0][0]

    if leader_name == previous_leader:

        return get_template(
            "LEADER_STATUS",
            leader=manager_case(leader_name)
        )

    return get_template(
        "LEADER_CHANGE",
        manager=manager_case(leader_name),
        manager_dat=manager_case(leader_name, "dat"),
        round=round_data["round"]
    )


# =========================
# GENERATE TABLE JUMP
# =========================

def generate_table_jump(round_data):

    current_round = round_data["round"]

    if current_round <= 1:
        return None

    previous = load_round(current_round - 1)

    if previous is None:
        return None

    current_ranking = get_ranking(round_data["table"])
    previous_ranking = get_ranking(previous["table"])

    current_positions = {}
    previous_positions = {}

    for i, team in enumerate(current_ranking):
        current_positions[team[0]] = i + 1

    for i, team in enumerate(previous_ranking):
        previous_positions[team[0]] = i + 1

    best_manager = None
    best_jump = 0

    for manager in current_positions:

        if manager not in previous_positions:
            continue

        jump = previous_positions[manager] - current_positions[manager]

        if jump > best_jump:
            best_jump = jump
            best_manager = manager

    if best_jump < 2:
        return None

    return get_template(
        "TABLE_JUMP",
        manager=manager_case(best_manager),
        jump=best_jump,
        position=current_positions[best_manager]
    )


# =========================
# GENERATE SPECIAL EVENT
# =========================


def generate_special_event(round_data):

    # sem budeme postupně přidávat zajímavosti

    event = generate_table_jump(round_data)

    if event:
        return event

    return generate_streak_section(round_data)


# =========================
# GENERATE STREAK SECTION
# =========================

def generate_streak_section(round_data):

    current_round = round_data["round"]

    if current_round < 3:
        return None

    streaks = {}

    # připrav manažery
    for manager in round_data["table"].keys():
        streaks[manager] = {
            "wins": 0,
            "without_win": 0
        }

    # projdi všechna odehraná kola
    for rnd in range(1, current_round + 1):

        data = load_round(rnd)

        if data is None:
            break

        for match in data["matches"]:

            home = match["home"]
            away = match["away"]

            hg = match["home_goals"]
            ag = match["away_goals"]

            if hg > ag:

                streaks[home]["wins"] += 1
                streaks[home]["without_win"] = 0

                streaks[away]["wins"] = 0
                streaks[away]["without_win"] += 1

            elif ag > hg:

                streaks[away]["wins"] += 1
                streaks[away]["without_win"] = 0

                streaks[home]["wins"] = 0
                streaks[home]["without_win"] += 1

            else:

                streaks[home]["wins"] = 0
                streaks[away]["wins"] = 0

                streaks[home]["without_win"] += 1
                streaks[away]["without_win"] += 1

    # hledání zajímavostí
    best_win = None
    best_win_count = 0

    longest_without = None
    longest_without_count = 0

    for manager, values in streaks.items():

        if values["wins"] > best_win_count:
            best_win = manager
            best_win_count = values["wins"]

        if values["without_win"] > longest_without_count:
            longest_without = manager
            longest_without_count = values["without_win"]

    if best_win_count >= 3:

        return get_template(
            "STREAK_WIN",
            manager=manager_case(best_win),
            count=best_win_count
        )

    if longest_without_count >= 4:
    
        return get_template(
            "STREAK_WITHOUT_WIN",
            manager=manager_case(longest_without),
            count=longest_without_count
        )

    return None