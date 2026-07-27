import json
import os
import random

from engine.results import load_round
from engine.standings import get_ranking


# =========================
# MANAGER NAME (CASE)
# =========================

def manager_accusative(name):

    names = {

        "Johnny": "Johnnyho",
        "Goran": "Gorana",
        "Kuba": "Kubu",
        "Matěj": "Matěje",
        "Matej": "Matěje",
        "Paulie": "Paulieho",
        "Francesco": "Francesca"

    }

    return names.get(name, name)


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
        generate_streak_section(round_data)
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
                    "headline":
                        f"{ranking[0][0]} se po {round_data['round']}. kole dostal do čela soutěže."
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

            winner = best_match["home"]
            loser = manager_accusative(best_match["away"])
            goals = (
                f"{best_match['home_goals']}:"
                f"{best_match['away_goals']}"
            )

        else:

            winner = best_match["away"]
            loser = manager_accusative(best_match["home"])
            goals = (
                f"{best_match['away_goals']}:"
                f"{best_match['home_goals']}"
            )

        templates = [

            f"{winner} porazil {loser} {goals} a zaznamenal nejvyšší výhru {round_data['round']}. kola.",

            f"Nejvyšší výhru {round_data['round']}. kola zaznamenal {winner}, který porazil {loser} {goals}.",

            f"{winner} předvedl nejpřesvědčivější výkon kola po výhře {goals} nad {loser}.",

            f"{winner} si připsal nejvyšší vítězství kola výsledkem {goals} proti {loser}."

        ]

        events.append({
            "priority": 50,
            "headline": random.choice(templates)
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
        f"{round_data['round']}. kolo nabídlo {matches} zápasy, "
        f"ve kterých padlo celkem {total_goals} branek."
    )

    if average >= 4:

        summary.append(
            f"Průměr {average} gólu na utkání potvrdil velmi ofenzivní průběh kola."
        )

    elif average >= 2.5:

        summary.append(
            f"Průměr {average} gólu na utkání nabídl vyrovnanou podívanou s několika zajímavými zápasy."
        )

    else:

        summary.append(
            f"Průměr {average} gólu na utkání ukázal, že tentokrát dominovaly především obrany."
        )

    if biggest_difference == 0:

        summary.append(
            "Všechna utkání skončila nerozhodně."
        )

    return summary


# =========================
# GENERATE PLAYER SECTION
# =========================

def generate_player_section(round_data):

    player = round_data["awards"]["player_of_round"]

    templates = [

        (
            f"Hráčem kola se stal {player['name']} "
            f"z {player['team']}, který získal známku {player['grade']}."
        ),

        (
            f"Nejlepší individuální výkon předvedl "
            f"{player['name']} ({player['team']}) "
            f"se známkou {player['grade']}."
        ),

        (
            f"Ocenění pro hráče kola putuje "
            f"{player['name']} z {player['team']}, "
            f"který obdržel známku {player['grade']}."
        )

    ]

    return random.choice(templates)


# =========================
# GENERATE MANAGER SECTION
# =========================

def generate_manager_section(round_data):

    manager = round_data["awards"]["manager_of_round"]

    templates = [

        (
            f"Manažerem kola se stal {manager['manager']}, "
            f"který nasbíral {manager['score']} bodů."
        ),

        (
            f"Nejlepší manažerský výkon předvedl {manager['manager']} "
            f"se ziskem {manager['score']} bodů."
        ),

        (
            f"Ocenění pro manažera kola získává {manager['manager']}, "
            f"který dosáhl na {manager['score']} bodů."
        )

    ]

    return random.choice(templates)


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

        return (
            f"Po úvodním kole vede soutěž {leader_name}."
        )

    previous_ranking = get_ranking(previous["table"])

    previous_leader = previous_ranking[0][0]

    if leader_name == previous_leader:

        return (
            f"V čele tabulky zůstává {leader_name}."
        )

    return (
        f"Do čela tabulky se dostal {leader_name}, "
        f"který vystřídal {previous_leader}."
    )


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
        return (
            f"{best_win} vyhrál už {best_win_count} zápasy v řadě."
        )

    if longest_without_count >= 4:
        return (
            f"{longest_without} čeká na vítězství už "
            f"{longest_without_count} kol."
        )

    return None