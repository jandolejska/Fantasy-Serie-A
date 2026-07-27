import json

from pathlib import Path


# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"


# =========================
# LOAD LEAGUE
# =========================

def load_league():

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

        managers.append(manager)

    return managers


# =========================
# PRINT LEAGUE
# =========================

def print_league():

    managers = load_league()

    print()
    print("=" * 40)
    print("STATISTIKY LIGY")
    print("=" * 40)

    for manager in managers:

        spent = sum(
            player["buy_price"]
            for player in manager["squad"]
        )

        budget = 333 - spent

        print()
        print(manager["name"])

        print(
            f"Trenér: {manager['coach']}"
        )

        print(
            f"Budget: {budget}"
        )

        print(
            f"Přestupy: {manager['transfers_left']}"
        )

        print(
            f"Hráčů: {len(manager['squad'])}"
        )

        print("-" * 40)