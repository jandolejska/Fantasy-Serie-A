import json
from pathlib import Path

from transfers.ownership import get_owned_players

# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

PLAYERS_FILE = (
    PROJECT_DIR /
    "data" /
    "players.json"
)


# =========================
# LOAD DATABASE
# =========================

def load_players():

    with open(
        PLAYERS_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# FIND PLAYER
# =========================

def find_player(players, name):

    for player in players:

        if player["name"].lower() == name.lower():

            return player

    return None


# =========================
# AVAILABLE PLAYERS
# =========================

def available_players(
    players,
    manager
):

    manager_players = {

        player["name"].lower()
        for player in manager["squad"]

    }

    owned_players = {

        name.lower()
        for name in get_owned_players()

    }

    available = []

    for player in players:

        # Odešlí hráči se nekupují
        if not player["active"]:
            continue

        # Už je v mé soupisce
        if player["name"].lower() in manager_players:
            continue

        # Vlastní ho jiný manažer
        if player["name"].lower() in owned_players:
            continue

        available.append(player)

    return available


# =========================
# FILTER ROLE
# =========================

def filter_role(
    players,
    role
):

    return [
        player
        for player in players
        if player["role"] == role
    ]


# =========================
# PLAYER PRICE
# =========================

def get_current_price(player):

    return player["qa"]


# =========================
# PLAYER INITIAL PRICE
# =========================

def get_initial_price(player):

    return player["qi"]


# =========================
# SEARCH PLAYERS
# =========================

def search_players(
    players,
    text,
    role=None
):

    text = text.lower().strip()

    results = []

    for player in players:

        if not player["active"]:
            continue

        if role is not None:

            if player["role"] != role:
                continue

        if text in player["name"].lower():

            results.append(player)

    results.sort(
        key=lambda x: x["name"]
    )

    return results