from engine.records import (
    load_records,
    save_records,
    print_records
)


# =========================
# CREATE STATISTICS
# =========================

def create_statistics(managers):

    stats = {}

    for manager in managers:

        stats[manager] = {
            "points": [],
            "goals_for": 0,
            "goals_against": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0
        }

    return stats


# =========================
# UPDATE STATISTICS
# =========================

def update_statistics(
    stats,
    home_name,
    away_name,
    home_score,
    away_score,
    home_goals,
    away_goals
):

    stats[home_name]["points"].append(home_score)
    stats[away_name]["points"].append(away_score)

    stats[home_name]["goals_for"] += home_goals
    stats[home_name]["goals_against"] += away_goals

    stats[away_name]["goals_for"] += away_goals
    stats[away_name]["goals_against"] += home_goals

    if home_goals > away_goals:

        stats[home_name]["wins"] += 1
        stats[away_name]["losses"] += 1

    elif home_goals < away_goals:

        stats[away_name]["wins"] += 1
        stats[home_name]["losses"] += 1

    else:

        stats[home_name]["draws"] += 1
        stats[away_name]["draws"] += 1


# =========================
# PRINT STATISTICS
# =========================

def print_statistics(stats):

    print("\n")
    print("=" * 40)
    print("STATISTIKY SEZÓNY")
    print("=" * 40)

    records = load_records()

    for manager, data in stats.items():

        average = sum(data["points"]) / len(data["points"])

        best = max(data["points"])
        worst = min(data["points"])

        print()

        print(manager)

        print(f"Průměr bodů: {average:.2f}")
        print(f"Nejvyšší skóre: {best:.1f}")
        print(f"Nejnižší skóre: {worst:.1f}")
        print(f"Skóre: {data['goals_for']}:{data['goals_against']}")
        print(
            f"Bilance: "
            f"{data['wins']}-{data['draws']}-{data['losses']}"
        )

        # =========================
        # RECORDS
        # =========================

        if best > records["highest_score"]["value"]:

            records["highest_score"] = {
                "manager": manager,
                "value": best
            }

        if data["goals_for"] > records["most_goals"]["value"]:

            records["most_goals"] = {
                "manager": manager,
                "value": data["goals_for"]
            }

        if average > records["best_average"]["value"]:

            records["best_average"] = {
                "manager": manager,
                "value": round(average, 2)
            }

    save_records(records)

    print_records(records)