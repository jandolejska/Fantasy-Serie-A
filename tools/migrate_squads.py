import json
from pathlib import Path

DATA_DIR = Path("data")
PLAYERS_FILE = DATA_DIR / "players.json"

# -------------------------------------------------------
# Načtení databáze hráčů
# -------------------------------------------------------

with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
    players = json.load(f)

players_by_name = {
    player["name"]: player
    for player in players
}

# -------------------------------------------------------
# Migrace všech squad.json
# -------------------------------------------------------

for squad_file in DATA_DIR.glob("*/squad.json"):

    print(f"\n📁 {squad_file}")

    with open(squad_file, "r", encoding="utf-8") as f:
        manager = json.load(f)

    updated = 0
    missing = []

    for player in manager["squad"]:

        db_player = players_by_name.get(player["name"])

        if db_player is None:
            missing.append(player["name"])
            continue

        # Zachovej kupní cenu
        buy_price = player["buy_price"]

        # Doplň informace z databáze
        player["id"] = db_player["id"]
        player["role"] = db_player["role"]
        player["team"] = db_player["team"]
        player["qa"] = db_player["qa"]
        player["qi"] = db_player["qi"]
        player["active"] = db_player["active"]

        # Kupní cena zůstává manažerovi
        player["buy_price"] = buy_price

        updated += 1

    with open(squad_file, "w", encoding="utf-8") as f:
        json.dump(manager, f, ensure_ascii=False, indent=4)

    print(f"   ✔ Aktualizováno: {updated}")

    if missing:
        print("   ⚠ Nenalezeni:")
        for name in missing:
            print(f"      - {name}")

print("\n✅ Hotovo.")