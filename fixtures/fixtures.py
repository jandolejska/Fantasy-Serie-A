import json

from pathlib import Path

from gameweek.gameweek import get_current_round


PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"

FIXTURES_DIR = DATA_DIR / "fixtures"


# =========================
# LOAD ROUND
# =========================

def load_round(round_number):

    file = FIXTURES_DIR / f"round_{round_number:02d}.json"

    if not file.exists():

        return []

    with open(
        file,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# NEXT ROUND
# =========================

def load_next_round():

    return load_round(
        get_current_round()
    )