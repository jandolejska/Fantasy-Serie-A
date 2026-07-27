import json
from pathlib import Path


# =========================
# FILES
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

PLAYERS_FILE = PROJECT_DIR / "data" / "players.json"

DATA_DIR = PROJECT_DIR / "data"


# =========================
# LOAD PLAYERS DATABASE
# =========================

with open(
    PLAYERS_FILE,
    encoding="utf-8"
) as f:

    players = json.load(f)


players_db = {}

for player in players:

    players_db[player["name"]] = player


print("=" * 40)
print("CONVERT SQUADS")
print("=" * 40)
print()


# =========================
# FIND MANAGERS
# =========================

manager_folders = []

for folder in DATA_DIR.iterdir():

    if not folder.is_dir():
        continue

    squad_file = folder / "squad.json"

    if squad_file.exists():

        manager_folders.append(folder)


# =========================
# CONVERT SQUADS
# =========================

converted = 0

for manager_folder in manager_folders:

    squad_file = manager_folder / "squad.json"

    with open(
        squad_file,
        encoding="utf-8"
    ) as f:

        squad = json.load(f)

    print(f"Zpracovávám: {squad['name']}")

    # přidání počtu přestupů
    squad["transfers_left"] = 4

    # doplnění buy_price
    for player in squad["squad"]:

        if player["name"] not in players_db:

            print(f"  Nenalezen hráč: {player['name']}")
            continue

        db_player = players_db[player["name"]]

        player["buy_price"] = db_player["qi"]

        converted += 1

    # uložení
    with open(
        squad_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            squad,
            f,
            ensure_ascii=False,
            indent=4
        )

    print("  ✔ Hotovo")


# =========================
# SUMMARY
# =========================

print()
print("=" * 40)
print("PŘEVOD DOKONČEN")
print("=" * 40)
print()

print(f"Manažerů: {len(manager_folders)}")
print(f"Hráčů upraveno: {converted}")

print()
print("Všem manažerům bylo přidáno:")
print("- transfers_left = 4")
print("- buy_price ke každému hráči")
print()