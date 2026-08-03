import json
from pathlib import Path
from shutil import copyfile


MANAGERS = [
    "johnny",
    "goran",
    "kuba",
    "francesco",
    "matej",
    "paulie"
]


# =========================
# RESET GAMEWEEK
# =========================

def reset_gameweek():

    path = Path("data/gameweek.json")

    data = {
        "current_round": 1,
        "completed_rounds": 0,
        "deadline": "",
        "locked": False
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


# =========================
# RESET PLAYER EVENTS
# =========================

def reset_player_events():

    path = Path(
        "data/player_events.json"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            [],
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================
# RESET NEWS
# =========================

def reset_news():

    path = Path(
        "data/current_news.json"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            [],
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================
# DELETE FILES
# =========================

def delete_files(folder, pattern):

    path = Path(folder)

    if not path.exists():
        return

    for file in path.glob(pattern):

        if file.is_file():

            file.unlink()


# =========================
# RESET REPORTS
# =========================

def reset_reports():

    delete_files(
        "reports",
        "round*.json"
    )


# =========================
# RESET RESULTS
# =========================

def reset_results():

    delete_files(
        "results",
        "round*.json"
    )


# =========================
# RESET LINEUPS
# =========================

def reset_lineups():

    for manager in MANAGERS:

        delete_files(
            f"data/{manager}/lineups",
            "round_*.json"
        )


# =========================
# RESET TRANSFERS
# =========================

def reset_transfers():

    for manager in MANAGERS:

        path = Path(
            f"data/{manager}/squad.json"
        )

        with open(
            path,
            encoding="utf-8"
        ) as f:

            squad = json.load(f)

        squad["transfers_left"] = 4

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                squad,
                f,
                indent=4,
                ensure_ascii=False
            )


# =========================
# START NEW SEASON
# =========================

def start_new_season():

    reset_gameweek()

    reset_player_events()

    reset_news()

    reset_reports()

    reset_results()

    reset_lineups()

    reset_transfers()

    return True


if __name__ == "__main__":

    start_new_season()

    print()

    print("================================")

    print(" Nová sezóna byla připravena.")

    print("================================")