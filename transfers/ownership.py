import json
from pathlib import Path


# =========================
# PATH
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"


# =========================
# OWNED PLAYERS
# =========================

def get_owned_players():

    owned = set()

    for folder in DATA_DIR.iterdir():

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

        for player in manager["squad"]:

            owned.add(
                player["name"]
            )

    return owned


# =========================
# OWNED COACHES
# =========================

def get_owned_coaches():

    owned = set()

    for folder in DATA_DIR.iterdir():

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

        owned.add(
            manager["coach"]
        )

    return owned