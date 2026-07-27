import json
import os

from engine.fantacalcio_downloader import download_grades
from engine.fantacalcio import parse
from gameweek.gameweek import get_current_round


def save_players(players, round_number):

    os.makedirs("data/grades", exist_ok=True)

    filename = f"data/grades/round{round_number}.json"

    with open(filename, "w", encoding="utf-8") as f:

        json.dump(
            players,
            f,
            ensure_ascii=False,
            indent=4
        )


def save_coaches(coaches, round_number):

    os.makedirs("data/coaches", exist_ok=True)

    filename = f"data/coaches/round{round_number}.json"

    with open(filename, "w", encoding="utf-8") as f:

        json.dump(
            coaches,
            f,
            ensure_ascii=False,
            indent=4
        )


def import_grades():

    round_number = get_current_round()

    download_grades()

    players, coaches = parse()

    save_players(
        players,
        round_number
    )

    save_coaches(
        coaches,
        round_number
    )

    return (
        len(players),
        len(coaches)
    )

def load_players(round_number):

    filename = f"data/grades/round{round_number}.json"

    with open(filename, encoding="utf-8") as f:

        return json.load(f)

def load_coaches(round_number):

    filename = f"data/coaches/round{round_number}.json"

    with open(filename, encoding="utf-8") as f:

        return json.load(f)