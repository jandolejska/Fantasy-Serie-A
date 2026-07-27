import json

from pathlib import Path

from serie_a.teams import get_team

from serie_a.fixtures import (
    get_current_round,
    get_next_opponent
)

# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"

PLAYERS_FILE = DATA_DIR / "players.json"

COACHES_FILE = DATA_DIR / "coaches.json"

# =========================
# LOAD PLAYERS DATABASE
# =========================

def load_players_database():

    with open(
        PLAYERS_FILE,
        encoding="utf-8"
    ) as f:

        players = json.load(f)

    database = {}

    for player in players:

        database[
            player["name"]
        ] = player

    return database


# =========================
# ENRICH SQUAD
# =========================

def enrich_squad(manager):

    database = load_players_database()

    for player in manager["squad"]:

        info = database.get(
            player["name"]
        )

        if info is None:
            continue

        player["team"] = info["team"]

        player["qa"] = info["qa"]

        player["qi"] = info["qi"]

        player["id"] = info["id"]

        player["active"] = info["active"]

        player["team_info"] = get_team(info["team"])

        player["fixture"] = get_next_opponent(
            info["team"],
            get_current_round()
        )

# =========================
# LOAD MANAGERS
# =========================

def load_managers():

    managers = []

    for folder in sorted(DATA_DIR.iterdir()):

        if not folder.is_dir():
            continue

        squad_file = folder / "squad.json"

        if not squad_file.exists():
            continue

        with open(
            squad_file,
            encoding="utf-8"
        ) as f:

            manager = json.load(f)

        enrich_squad(
            manager
        )

        spent = sum(
            player["buy_price"]
            for player in manager["squad"]
        )

        manager["budget"] = 333 - spent

        manager["slug"] = folder.name

        managers.append(manager)

    return managers


# =========================
# LOAD MANAGER
# =========================

def load_manager_web(slug):

    squad_file = (
        DATA_DIR /
        slug /
        "squad.json"
    )

    if not squad_file.exists():

        return None

    with open(
        squad_file,
        encoding="utf-8"
    ) as f:

        manager = json.load(f)

    enrich_squad(
        manager
    )

    spent = sum(
        player["buy_price"]
        for player in manager["squad"]
    )

    manager["budget"] = 333 - spent

    manager["slug"] = slug

    return manager


# =========================
# LEAGUE SUMMARY
# =========================

def get_league_summary():

    managers = load_managers()

    total_players = sum(
        len(manager["squad"])
        for manager in managers
    )

    return {

        "managers": len(managers),

        "players": total_players,

        "transfers": "Otevřené"

    }


# =========================
# LOAD COACHES
# =========================

def load_coaches():

    with open(
        COACHES_FILE,
        encoding="utf-8"
    ) as f:

        coaches = json.load(f)

    coaches.sort()

    return coaches