import json
import os

from gameweek.gameweek import (
    get_current_round,
    get_completed_rounds
)

# =========================
# CREATE RESULTS FOLDER
# =========================

def create_results_folder():

    os.makedirs("results", exist_ok=True)


# =========================
# SAVE ROUND
# =========================

def save_round(
    round_number,
    matches,
    lineups=None,
    table=None,
    awards=None
):

    create_results_folder()

    data = {
        "version": 1,
        "round": round_number,
        "matches": matches,
        "lineups": lineups or {},
        "table": table or [],
        "awards": awards or {}
    }

    with open(
        f"results/round{round_number}.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================
# LOAD ROUND
# =========================

def load_round(round_number):

    file = f"results/round{round_number}.json"

    if not os.path.exists(file):

        return None

    with open(
        file,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# LOAD ALL ROUNDS
# =========================

def load_all_rounds():

    rounds = []

    current_round = get_current_round()

    for round_number in range(1, current_round):

        data = load_round(round_number)

        if data:

            rounds.append(data)

    return rounds


# =========================
# LOAD LAST ROUND
# =========================

def load_last_round():

    completed = get_completed_rounds()

    if completed == 0:
        return []

    data = load_round(completed)

    if not data:
        return []

    return data["matches"]


# =========================
# LOAD NEXT ROUND
# =========================

def load_next_round():

    data = load_round(get_current_round())

    if not data:
        return []

    return data["matches"]


# =========================
# LOAD FIXTURE
# =========================

def load_fixture():

    base_dir = os.path.dirname(os.path.dirname(__file__))

    fixture_file = os.path.join(
        base_dir,
        "data",
        "fixtures.json"
    )

    with open(
        fixture_file,
        encoding="utf-8"
    ) as f:

        fixture = json.load(f)

    rounds = []

    for round_data in fixture:

        played = load_round(
            round_data["round"]
        )

        played_matches = {}

        if played:

            for match in played["matches"]:

                key = (
                    match["home"],
                    match["away"]
                )

                played_matches[key] = match

        matches = []

        for home, away in round_data["matches"]:

            result = played_matches.get(
                (home, away)
            )

            if result:

                matches.append(result)

            else:

                matches.append({

                    "home": home,
                    "away": away,

                    "home_slug": home.lower(),
                    "away_slug": away.lower(),

                    "home_goals": None,
                    "away_goals": None,

                    "home_score": None,
                    "away_score": None

                })

        rounds.append({

            "round": round_data["round"],
            "matches": matches

        })

    return rounds