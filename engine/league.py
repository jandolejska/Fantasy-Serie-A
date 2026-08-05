import json

from engine.match import play_manager
from engine.standings import (
    create_table,
    update_table,
    print_table,
    load_round
)
from engine.coach import get_coach_grade
from engine.calculator import score_to_goals, grade_to_float
from engine.results import save_round
from engine.awards import (
    print_manager_award,
    print_player_award,
    print_team_of_round
)
from engine.statistics import (
    create_statistics,
    update_statistics,
    print_statistics
)
from engine.records import (
    load_records,
    save_records
)
from gameweek.gameweek import (
    get_current_round,
    set_completed_round
)
from engine.manager import has_round
from engine.import_grades import load_players
from engine.report import generate_round_report
from news.news import clear_news

# =========================
# LOAD FIXTURES
# =========================

def load_fixtures():

    with open("data/fixtures.json", encoding="utf-8") as f:
        return json.load(f)


# =========================
# PRINT TEAM
# =========================

def print_team(team, home=False, coach_bonus=0):

    print("\nBody hráčů:\n")

    players_sum = 0

    for player in team["starting"]:

        if player["grade"] is None:
            print(f"{player['name']:<20} -")
            continue

        grade = grade_to_float(player["grade"])
        players_sum += grade

        print(f"{player['name']:<20} {grade}")

    print("-" * 30)
    print(f"Součet hráčů: {players_sum}")

    total = players_sum

    if home:
        total += 2
        print("Domácí bonus: +2")

    if coach_bonus > 0:
        total += coach_bonus
        print(f"Bonus trenéra: +{coach_bonus}")

    print("-" * 30)
    print(f"Celkem: {total}\n")


# =========================
# PLAY ONE ROUND
# =========================

def play_round(round_data, players, table, stats):

    print("\n========================================")
    print(f"ROUND {round_data['round']}")
    print("========================================\n")

    results = []

    records = load_records()

    for home_name, away_name in round_data["matches"]:

        print("----------------------------------------")
        print(f"{home_name} vs {away_name}")
        print("----------------------------------------")

        home = play_manager(
            home_name,
            round_data["round"],
            players,
            home=True
        )

        away = play_manager(
            away_name,
            round_data["round"],
            players
        )

        home_raw_score = home["score"] - 2
        away_raw_score = away["score"]

        home_bonus = 0
        away_bonus = 0

        home_grade = get_coach_grade(
            home["manager"]["coach"],
            round_data["round"]
        )

        away_grade = get_coach_grade(
            away["manager"]["coach"],
            round_data["round"]
        )

        if home_grade > away_grade:

            home_bonus = 0.5
            home["score"] += 0.5

            print(
                f"\nBonus trenéra: {home_name} "
                f"(+0.5, {home['manager']['coach']} {home_grade} > "
                f"{away['manager']['coach']} {away_grade})"
            )

        elif away_grade > home_grade:

            away_bonus = 0.5
            away["score"] += 0.5

            print(
                f"\nBonus trenéra: {away_name} "
                f"(+0.5, {away['manager']['coach']} {away_grade} > "
                f"{home['manager']['coach']} {home_grade})"
            )

        home["goals"] = score_to_goals(home["score"])
        away["goals"] = score_to_goals(away["score"])

        print_team(
            home,
            home=True,
            coach_bonus=home_bonus
        )

        print_team(
            away,
            coach_bonus=away_bonus
        )

        print(
            f"{home_name} {home['goals']} : "
            f"{away['goals']} {away_name}\n"
        )

        update_table(
            table,
            home_name,
            away_name,
            home["goals"],
            away["goals"]
        )

        update_statistics(
            stats,
            home_name,
            away_name,
            home["score"],
            away["score"],
            home["goals"],
            away["goals"]
        )

        # =========================
        # RECORD - BIGGEST WIN
        # =========================

        difference = abs(
            home["goals"] - away["goals"]
        )

        if difference > records["biggest_win"]["difference"]:

            records["biggest_win"] = {

                "match":
                    f"{home_name} "
                    f"{home['goals']}:{away['goals']} "
                    f"{away_name}",

                "difference": difference

            }

        results.append({

            "home": home_name,
            "away": away_name,

            "home_slug": home_name.lower(),
            "away_slug": away_name.lower(),

            "home_team": home,
            "away_team": away,

            "home_score": home["score"],
            "away_score": away["score"],

            "home_goals": home["goals"],
            "away_goals": away["goals"],

            "home_coach_grade": home_grade,
            "away_coach_grade": away_grade,

            "home_bonus": home_bonus,
            "away_bonus": away_bonus,

            "home_raw_score": home_raw_score,
            "away_raw_score": away_raw_score,

            "home_home_bonus": 2,
            "away_home_bonus": 0,

            "home_substitutions": home["substitutions"],
            "away_substitutions": away["substitutions"]

        })

    save_records(records)

    manager_award = print_manager_award(
        round_data["round"],
        results
    )

    player_award = print_player_award(
        round_data["round"],
        players
    )

    team_award = print_team_of_round(
        players
    )

    awards = {
        "manager_of_round": manager_award,
        "player_of_round": player_award,
        "team_of_round": team_award
    }

    save_round(
        round_data["round"],
        results,
        table=table,
        awards=awards
    )

    generate_round_report(
        round_data["round"]
    )

    set_completed_round(
        round_data["round"]
    )    

    return table


# =========================
# PLAY WHOLE SEASON
# =========================

def play_season(players):

    fixtures = load_fixtures()

    managers = []

    for fixture in fixtures:

        for home, away in fixture["matches"]:

            if home not in managers:
                managers.append(home)

            if away not in managers:
                managers.append(away)

    previous_round = load_round(current_round - 1)

    if previous_round is not None:
        table = previous_round["table"]
    else:
        table = create_table(managers)

    stats = create_statistics(managers)

    for fixture in fixtures:

        table = play_round(
            fixture,
            players,
            table,
            stats
        )

    print_table(table)

    print_statistics(stats)


# =========================
# CHECK ROUND READY
# =========================

def check_round_ready():

    fixtures = load_fixtures()

    current_round = get_current_round()

    for fixture in fixtures:

        if fixture["round"] != current_round:
            continue

        for home, away in fixture["matches"]:
            
            print(f"Kontrola: {home} vs {away}")
            print(f"Aktuální kolo: {current_round}")

            if not has_round(home, current_round):
                return False, home

            if not has_round(away, current_round):
                return False, away

        return True, None

    return False, None


# =========================
# PLAY CURRENT ROUND
# =========================

def play_current_round():

    ready, manager = check_round_ready()

    if not ready:
        return False, manager

    fixtures = load_fixtures()

    current_round = get_current_round()

    players = load_players(current_round)

    managers = []

    for fixture in fixtures:

        for home, away in fixture["matches"]:

            if home not in managers:
                managers.append(home)

            if away not in managers:
                managers.append(away)

    previous_round = load_round(current_round - 1)

    if previous_round is not None:
        table = previous_round["table"]
    else:
        table = create_table(managers)

    stats = create_statistics(managers)

    played = False

    for fixture in fixtures:

        if fixture["round"] == current_round:

            table = play_round(
                fixture,
                players,
                table,
                stats
            )

            played = True
            break

    if not played:
        return False

    print_table(table)
    print_statistics(stats)

    try:
        clear_news()
    except Exception as e:
        print(f"Chyba při mazání novinek: {e}")

    return True, None