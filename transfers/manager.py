import json
from pathlib import Path


# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"


# =========================
# GET MANAGERS
# =========================

def get_manager_names():

    managers = []

    for folder in DATA_DIR.iterdir():

        if not folder.is_dir():
            continue

        squad_file = folder / "squad.json"

        if squad_file.exists():

            managers.append(folder.name.title())

    managers.sort()

    return managers


# =========================
# LOAD MANAGER
# =========================

def load_manager(manager_name):

    manager_folder = DATA_DIR / manager_name

    squad_file = manager_folder / "squad.json"

    with open(
        squad_file,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# SAVE MANAGER
# =========================

def save_manager(manager):

    squad_file = (
        DATA_DIR /
        manager["slug"] /
        "squad.json"
    )

    manager_to_save = manager.copy()
    manager_to_save.pop("slug", None)

    with open(
        squad_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            manager_to_save,
            f,
            ensure_ascii=False,
            indent=4
        )

# =========================
# FIND PLAYER
# =========================

def find_player(manager, player_name):

    for player in manager["squad"]:

        if player["name"].lower() == player_name.lower():

            return player

    return None


# =========================
# REMOVE PLAYER
# =========================

def remove_player(manager, player_name):

    player = find_player(
        manager,
        player_name
    )

    if player is None:
        return False

    manager["squad"].remove(player)

    return True


# =========================
# ADD PLAYER
# =========================

def add_player(manager, player):

    manager["squad"].append(player)


# =========================
# REPLACE PLAYER
# =========================

def replace_player(
    manager,
    old_player,
    new_player
):

    squad = manager["squad"]

    for i, player in enumerate(squad):

        if player["name"] == old_player["name"]:

            squad[i] = new_player
            return True

    return False