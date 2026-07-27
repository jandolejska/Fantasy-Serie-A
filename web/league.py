import json

from pathlib import Path


# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"

LEAGUE_FILE = DATA_DIR / "league.json"


# =========================
# LOAD LEAGUE
# =========================

def load_league():

    with open(
        LEAGUE_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# STANDINGS
# =========================

def get_standings():

    league = load_league()

    return league["standings"]


# =========================
# SEASON
# =========================

def get_season():

    league = load_league()

    return league["season"]