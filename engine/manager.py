import json

from pathlib import Path

# =========================
# LOAD FILES
# =========================

def load_squad(manager_name):

    with open(
        f"data/{manager_name}/squad.json",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def load_round(manager_name, round_number):

    with open(
        f"data/{manager_name}/lineups/round_{round_number:02d}.json",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def load_manager(manager_name):

    return load_squad(manager_name)


# =========================
# HAS ROUND
# =========================

def has_round(manager_name, round_number):

    return find_latest_round(
        manager_name,
        round_number
    ) is not None


# =========================
# FIND PLAYER
# =========================

def find_player(name, players):

    for player in players:

        if player["name"].lower() == name.lower():
            return player

    return None


# =========================
# FIND ROLE
# =========================

def find_role(name, squad):

    for player in squad["squad"]:

        if player["name"].lower() == name.lower():
            return player["role"]

    return ""


# =========================
# FIND LATEST ROUND
# =========================

def find_latest_round(manager_name, round_number):
    """
    Vrátí číslo posledního kola, pro které existuje uložená sestava.
    """

    for rnd in range(round_number, 0, -1):

        path = Path(
            f"data/{manager_name}/lineups/round_{rnd:02d}.json"
        )

        if path.exists():
            return rnd

    return None


# =========================
# BUILD TEAM
# =========================

def build_team(manager_name, round_number, players):

    manager = load_manager(manager_name)
    latest_round = find_latest_round(
        manager_name,
        round_number
    )

    if latest_round is None:
        raise FileNotFoundError(
            f"{manager_name} nemá uloženou žádnou sestavu."
        )

    round_data = load_round(
        manager_name,
        latest_round
    )

    starting = []
    bench = []

    # =========================
    # STARTING
    # =========================

    for name in round_data["starting"]:

        player = find_player(name, players)

        if player:

            starting.append({

                "name": player["name"],
                "role": player["role"],
                "grade": player["grade"]

            })

        else:

            starting.append({

                "name": name,
                "role": find_role(name, manager),
                "grade": None

            })

    # =========================
    # BENCH
    # =========================

    for name in round_data["bench"]:

        player = find_player(name, players)

        if player:

            bench.append({

                "name": player["name"],
                "role": player["role"],
                "grade": player["grade"]

            })

        else:

            bench.append({

                "name": name,
                "role": find_role(name, manager),
                "grade": None

            })

    return manager, starting, bench