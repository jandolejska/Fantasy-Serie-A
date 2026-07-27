import json


# =========================
# LOAD FIXTURES
# =========================

def load_fixtures():

    with open("data/fixtures.json", encoding="utf-8") as f:
        return json.load(f)


# =========================
# LOAD ROUND
# =========================

def load_round(round_number):

    try:

        with open(
            f"results/round{round_number}.json",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except FileNotFoundError:

        return None

# =========================
# CREATE TABLE
# =========================

def create_table(managers):

    table = {}

    for manager in managers:

        table[manager] = {
            "points": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0
        }

    return table


# =========================
# UPDATE TABLE
# =========================

def update_table(table, home, away, home_goals, away_goals):

    table[home]["goals_for"] += home_goals
    table[home]["goals_against"] += away_goals

    table[away]["goals_for"] += away_goals
    table[away]["goals_against"] += home_goals

    if home_goals > away_goals:

        table[home]["wins"] += 1
        table[away]["losses"] += 1
        table[home]["points"] += 3

    elif home_goals < away_goals:

        table[away]["wins"] += 1
        table[home]["losses"] += 1
        table[away]["points"] += 3

    else:

        table[home]["draws"] += 1
        table[away]["draws"] += 1

        table[home]["points"] += 1
        table[away]["points"] += 1

    return table


# =========================
# PRINT TABLE
# =========================

def print_table(table):

    print("\n========================================")
    print("TABULKA")
    print("========================================")

    ranking = get_ranking(table)

    print(f"{'Poř.':<5}{'Tým':<12}{'B':>4}{'V':>4}{'R':>4}{'P':>4}{'Skóre':>10}")

    for i, (name, stats) in enumerate(ranking, 1):

        score = f"{stats['goals_for']}:{stats['goals_against']}"

        print(
            f"{i:<5}"
            f"{name:<12}"
            f"{stats['points']:>4}"
            f"{stats['wins']:>4}"
            f"{stats['draws']:>4}"
            f"{stats['losses']:>4}"
            f"{score:>10}"
        )


# =========================
# GET RANKING
# =========================

def get_ranking(table):

    return sorted(
        table.items(),
        key=lambda x: (
            x[1]["points"],
            x[1]["goals_for"] - x[1]["goals_against"],
            x[1]["goals_for"]
        ),
        reverse=True
    )


# =========================
# CALCULATE TABLE
# =========================

def calculate_table():

    fixtures = load_fixtures()

    managers = []

    for fixture in fixtures:

        for home, away in fixture["matches"]:

            if home not in managers:
                managers.append(home)

            if away not in managers:
                managers.append(away)

    table = create_table(managers)

    for fixture in fixtures:

        results = load_round(fixture["round"])

        if results is None:
            break

        for match in results["matches"]:

            update_table(
                table,
                match["home"],
                match["away"],
                match["home_goals"],
                match["away_goals"]
            )

    return get_ranking(table)