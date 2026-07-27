import json
from pathlib import Path

from serie_a.teams import get_team

# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

FIXTURES_FILE = (
    PROJECT_DIR /
    "data" /
    "serie_a" /
    "fixtures.json"
)

# =========================
# LOAD FIXTURES
# =========================

def load_fixtures():

    with open(
        FIXTURES_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)

# =========================
# CURRENT ROUND
# =========================

def get_current_round():

    return 1


# =========================
# NEXT OPPONENT
# =========================

def get_next_opponent(team, round_number):

    fixtures = load_fixtures()

    for round_data in fixtures:

        if round_data["round"] != round_number:
            continue

        for match in round_data["matches"]:

            if match["home"] == team:

                opponent = get_team(match["away"])

                return {
                    "opponent": match["away"],
                    "home": True,
                    "short": opponent["short"],
                    "logo": opponent["logo"]
                }

            if match["away"] == team:

                opponent = get_team(match["home"])

                return {
                    "opponent": match["home"],
                    "home": False,
                    "short": opponent["short"],
                    "logo": opponent["logo"]
                }

    return None


# =========================
# NEXT OPPONENT (CURRENT ROUND)
# =========================

def get_current_opponent(team):

    return get_next_opponent(
        team,
        get_current_round()
    )