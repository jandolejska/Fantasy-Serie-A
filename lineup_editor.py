import json
import os


# =========================
# FORMACE
# =========================

FORMATIONS = {
    1: (3, 4, 3),
    2: (3, 5, 2),
    3: (4, 3, 3),
    4: (4, 4, 2),
    5: (4, 5, 1),
    6: (5, 3, 2),
    7: (5, 4, 1)
}


# =========================
# LOAD MANAGER
# =========================

manager_name = input("Manažer: ")

with open(
    f"data/{manager_name}/squad.json",
    encoding="utf-8"
) as f:

    manager = json.load(f)


round_number = int(
    input("Kolo: ")
)


print("\n========================================")
print("LINEUP EDITOR")
print("========================================")

print("\nRozestavení:\n")

print("1) 3-4-3")
print("2) 3-5-2")
print("3) 4-3-3")
print("4) 4-4-2")
print("5) 4-5-1")
print("6) 5-3-2")
print("7) 5-4-1")

formation = int(input("\n> "))

defenders, midfielders, attackers = FORMATIONS[formation]


# =========================
# ROZDĚLENÍ HRÁČŮ
# =========================

goalkeepers = []
defenders_list = []
midfielders_list = []
attackers_list = []

for player in manager["squad"]:

    if player["role"] == "P":
        goalkeepers.append(player)

    elif player["role"] == "D":
        defenders_list.append(player)

    elif player["role"] == "C":
        midfielders_list.append(player)

    elif player["role"] == "A":
        attackers_list.append(player)


# =========================
# VÝBĚR HRÁČŮ
# =========================

def choose_players(players, count, title):

    print(f"\n{title}\n")

    for i, player in enumerate(players, start=1):
        print(f"{i}. {player['name']}")

    while True:

        choice = input("\n> ").split()

        if len(choice) != count:
            print(f"Vyber přesně {count} hráčů.")
            continue

        try:
            indexes = [int(x) - 1 for x in choice]

        except ValueError:
            print("Neplatný vstup.")
            continue

        if len(set(indexes)) != len(indexes):
            print("Hráče nelze vybrat dvakrát.")
            continue

        if min(indexes) < 0 or max(indexes) >= len(players):
            print("Neplatné číslo.")
            continue

        selected = []

        for index in indexes:
            selected.append(players[index])

        return selected


# =========================
# ZÁKLADNÍ SESTAVA
# =========================

starting = []

starting += choose_players(
    goalkeepers,
    1,
    "Vyber brankáře"
)

starting += choose_players(
    defenders_list,
    defenders,
    f"Vyber {defenders} obránce"
)

starting += choose_players(
    midfielders_list,
    midfielders,
    f"Vyber {midfielders} záložníky"
)

starting += choose_players(
    attackers_list,
    attackers,
    f"Vyber {attackers} útočníky"
)


# =========================
# LAVIČKA
# =========================

available_bench = []

for player in manager["squad"]:

    in_starting = False

    for starter in starting:

        if starter["name"] == player["name"]:
            in_starting = True
            break

    if not in_starting:
        available_bench.append(player)


while True:

    try:

        bench_count = int(
            input("\nKolik hráčů chceš na lavičku? (0-7)\n\n> ")
        )

    except ValueError:

        print("Zadej číslo.")
        continue

    if 0 <= bench_count <= 7:
        break

    print("Lavička může mít maximálně 7 hráčů.")


bench = []

if bench_count > 0:

    print(f"\nVyber {bench_count} náhradníků")
    print("(pořadí = pořadí střídání)\n")

    for i, player in enumerate(available_bench, start=1):

        print(
            f"{i}. {player['name']} ({player['role']})"
        )

    while True:

        choice = input("\n> ").split()

        if len(choice) != bench_count:

            print(
                f"Vyber přesně {bench_count} hráčů."
            )
            continue

        try:

            indexes = [int(x) - 1 for x in choice]

        except ValueError:

            print("Neplatný vstup.")
            continue

        if len(set(indexes)) != len(indexes):

            print("Hráče nelze vybrat dvakrát.")
            continue

        if min(indexes) < 0 or max(indexes) >= len(available_bench):

            print("Neplatné číslo.")
            continue

        for index in indexes:
            bench.append(
                available_bench[index]
            )

        break


# =========================
# ROUND DATA
# =========================

round_data = {

    "formation": f"{defenders}-{midfielders}-{attackers}",

    "starting": [

        player["name"]

        for player in starting

    ],

    "bench": [

        player["name"]

        for player in bench

    ]
}


# =========================
# SAVE
# =========================

folder = f"data/{manager_name}"

os.makedirs(
    folder,
    exist_ok=True
)

with open(
    f"{folder}/round{round_number}.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        round_data,
        f,
        ensure_ascii=False,
        indent=4
    )


# =========================
# PRINT
# =========================

print("\n========================================")
print("SESTAVA ULOŽENA")
print("========================================")

print(f"\nManažer: {manager_name}")
print(f"Kolo: {round_number}")
print(f"Rozestavení: {round_data['formation']}")

print("\nZákladní sestava:\n")

for player in starting:

    print(player["name"])

print("\nLavička:\n")

if bench:

    for player in bench:

        print(player["name"])

else:

    print("(bez náhradníků)")

print(
    f"\nSoubor uložen jako:\n"
    f"data/{manager_name}/round{round_number}.json"
)