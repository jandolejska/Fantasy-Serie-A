import json

from pathlib import Path


# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"

RESULTS_DIR = DATA_DIR / "results"


# =========================
# LOAD ROUND RESULTS
# =========================

def load_round_results(round_number):

    file = RESULTS_DIR / f"round_{round_number:02d}.json"

    if not file.exists():

        return []

    with open(
        file,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# LAST RESULTS
# =========================

def load_last_results():

    from gameweek.gameweek import get_current_round

    round_number = get_current_round()

    if round_number <= 1:

        return []

    return load_round_results(
        round_number - 1
    )


# =========================
# ALL RESULTS
# =========================

def load_all_results():

    from gameweek.gameweek import get_current_round

    results = []

    for round_number in range(1, get_current_round()):

        matches = load_round_results(round_number)

        if matches:

            results.append({

                "round": round_number,

                "matches": matches

            })

    return results