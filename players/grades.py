import json
import os


ROUNDS_DIR = "results"


def load_player_grades(player_id):

    grades = []

    if not os.path.exists(ROUNDS_DIR):
        return grades

    files = sorted(
        f for f in os.listdir(ROUNDS_DIR)
        if f.startswith("round") and f.endswith(".json")
    )

    for filename in files:

        path = os.path.join(
            ROUNDS_DIR,
            filename
        )

        with open(
            path,
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        round_number = data["round"]

        grade = None

        for match in data["matches"]:

            for side in (
                "home_team",
                "away_team"
            ):

                # základní sestava
                for player in match[side]["starting"]:

                    if (
                        player["name"]
                        ==
                        get_player_name(player_id)
                    ):

                        grade = player["grade"]

                # lavička
                for player in match[side]["bench"]:

                    if (
                        player["name"]
                        ==
                        get_player_name(player_id)
                    ):

                        if grade is None:
                            grade = player["grade"]

        grades.append({

            "round": round_number,

            "grade": grade

        })

    return grades

from players.service import get_player


def get_player_name(player_id):

    player = get_player(player_id)

    return player["name"]