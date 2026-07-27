import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

TEAMS_FILE = (
    PROJECT_DIR
    / "data"
    / "teams.json"
)


def load_teams():

    with open(
        TEAMS_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


teams = load_teams()


def get_team(team_name):

    return teams.get(team_name)