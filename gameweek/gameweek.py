import json

from pathlib import Path

from datetime import datetime

# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"

GAMEWEEK_FILE = DATA_DIR / "gameweek.json"

FIXTURES_FILE = DATA_DIR / "fixtures.json"


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
# NEXT ROUND FIXTURES
# =========================

def get_next_round_fixtures():

    next_round = get_completed_rounds() + 1

    fixtures = load_fixtures()

    for fixture in fixtures:

        if fixture["round"] == next_round:

            matches = []

            for home, away in fixture["matches"]:

                matches.append({

                    "home": home,
                    "away": away

                })

            return matches

    return []


# =========================
# LOAD GAMEWEEK
# =========================

def load_gameweek():

    with open(
        GAMEWEEK_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# CURRENT ROUND
# =========================

def get_current_round():

    gameweek = load_gameweek()

    return gameweek["current_round"]


# =========================
# DEADLINE
# =========================

def get_deadline():

    data = load_gameweek()

    return data["deadline"]


# =========================
# LOCKED
# =========================

def is_lineup_locked():

    gameweek = load_gameweek()

    return gameweek["locked"]


# =========================
# SAVE GAMEWEEK
# =========================

def save_gameweek(data):

    with open(
        GAMEWEEK_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


# =========================
# OPEN NEW ROUND
# =========================

def open_new_round(deadline):

    print("OPEN_NEW_ROUND DEADLINE =", repr(deadline))

    gameweek = load_gameweek()

    fixtures = load_fixtures()
    total_rounds = len(fixtures)

    if gameweek["current_round"] >= total_rounds:
        return False

    gameweek["current_round"] += 1
    gameweek["deadline"] = deadline
    gameweek["locked"] = False

    print(gameweek)

    save_gameweek(gameweek)

    return True


# =========================
# SET LOCK
# =========================

def set_lineup_locked(locked):

    gameweek = load_gameweek()

    gameweek["locked"] = locked

    save_gameweek(gameweek)


# =========================
# AUTO LOCK
# =========================

def auto_lock_lineups():

    gameweek = load_gameweek()

    print("===== AUTO LOCK =====")
    print("Locked:", gameweek["locked"])
    print("Deadline:", gameweek["deadline"])

    if gameweek["locked"]:
        print("Už zamčeno")
        return

    if not gameweek["deadline"]:
        print("Deadline není nastaven")
        return

    deadline = datetime.fromisoformat(
        gameweek["deadline"]
    )

    now = datetime.now()

    print("NOW:", now)
    print("DEADLINE:", deadline)

    if now >= deadline:

        print(">>> ZAMYKÁM <<<")

        gameweek["locked"] = True

        save_gameweek(gameweek)


# =========================
# COMPLETED ROUNDS
# =========================

def get_completed_rounds():

    gameweek = load_gameweek()

    return gameweek["completed_rounds"]


# =========================
# SET COMPLETED ROUNDS
# =========================

def set_completed_round(round_number):

    gameweek = load_gameweek()

    gameweek["completed_rounds"] = round_number

    save_gameweek(gameweek)