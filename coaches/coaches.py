import json
from pathlib import Path

DATA_FILE = Path("data/coaches.json")


def load_coaches():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_coaches(coaches):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(coaches, f, ensure_ascii=False, indent=4)


def get_coach(name):
    coaches = load_coaches()
    return coaches.get(name)