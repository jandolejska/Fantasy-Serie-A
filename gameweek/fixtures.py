import json

from pathlib import Path


FIXTURES_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "fixtures.json"
)


# =========================
# LOAD FIXTURES
# =========================

def load_fixtures():

    with open(
        FIXTURES_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# LOAD ROUND FIXTURES
# =========================

def load_round_fixtures(round_number):

    fixtures = load_fixtures()

    for round_data in fixtures:

        if round_data["round"] == round_number:

            return round_data["matches"]

    return []
