import json
from pathlib import Path


LEAGUE_FILE = Path("data/league.json")


def load_league():

    with open(
        LEAGUE_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_league(data):

    with open(
        LEAGUE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def get_season():

    return load_league()["season"]


def set_season(season):

    league = load_league()

    league["season"] = season

    save_league(league)