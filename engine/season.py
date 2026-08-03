import json
from pathlib import Path


# =========================
# LOAD SEASON
# =========================

def load_season():

    path = Path(
        "data/league.json"
    )

    with open(
        path,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# GET SEASON
# =========================

def get_season():

    return load_season()["season"]


# =========================
# SET SEASON
# =========================

def set_season(season):

    path = Path(
        "data/league.json"
    )

    data = {
        "season": season
    }

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )