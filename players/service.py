import json
import os


PLAYERS_FILE = "data/players.json"
TEAMS_FILE = "data/teams.json"

MANAGERS = [
    "johnny",
    "goran",
    "kuba",
    "francesco",
    "matej",
    "paulie"
]


def load_players():

    with open(
        PLAYERS_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


def get_player(player_id):

    player_id = int(player_id)

    teams = load_teams()

    for player in load_players():

        if int(player["id"]) == player_id:

            player = player.copy()

            player["team_info"] = teams.get(
                player["team"],
                {}
            )

            return player

    return None


def get_player_owner(player_id):

    player_id = int(player_id)

    for manager in MANAGERS:

        path = f"data/{manager}/squad.json"

        if not os.path.exists(path):
            continue

        with open(path, encoding="utf-8") as f:

            squad = json.load(f)

        for player in squad["squad"]:

            if int(player.get("id", -1)) == player_id:

                return squad

    return None

def load_teams():

    with open(
        TEAMS_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)