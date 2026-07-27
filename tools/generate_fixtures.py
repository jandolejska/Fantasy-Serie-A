import json
from pathlib import Path


# =========================
# SETTINGS
# =========================

MANAGERS = [
    "Johnny",
    "Goran",
    "Francesco",
    "Matej",
    "Kuba",
    "Paulie"
]

TOTAL_ROUNDS = 38


# =========================
# ROUND ROBIN
# =========================

def generate_round_robin(managers):

    teams = managers[:]

    if len(teams) % 2 != 0:
        teams.append("BYE")

    rounds = []

    n = len(teams)

    for round_number in range(n - 1):

        matches = []

        for i in range(n // 2):

            home = teams[i]
            away = teams[n - 1 - i]

            if home == "BYE" or away == "BYE":
                continue

            # střídání domácí/venkovní výhody
            if round_number % 2 == 0:
                matches.append([home, away])
            else:
                matches.append([away, home])

        rounds.append(matches)

        # rotace týmů
        teams = (
            [teams[0]]
            + [teams[-1]]
            + teams[1:-1]
        )

    return rounds


# =========================
# HOME / AWAY
# =========================

def generate_cycle(managers):

    first_half = generate_round_robin(managers)

    second_half = []

    for matches in first_half:

        rematch = []

        for home, away in matches:
            rematch.append([away, home])

        second_half.append(rematch)

    return first_half + second_half


# =========================
# BUILD SEASON
# =========================

def build_season(managers, total_rounds):

    cycle = generate_cycle(managers)

    fixtures = []

    round_number = 1

    while len(fixtures) < total_rounds:

        for matches in cycle:

            if len(fixtures) >= total_rounds:
                break

            fixtures.append({
                "round": round_number,
                "matches": matches
            })

            round_number += 1

    return fixtures


# =========================
# SAVE
# =========================

def save(fixtures):

    path = Path("data/fixtures.json")

    with open(path, "w", encoding="utf-8") as f:

        json.dump(
            fixtures,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    fixtures = build_season(
        MANAGERS,
        TOTAL_ROUNDS
    )

    save(fixtures)

    print(f"Vygenerováno {len(fixtures)} kol.")