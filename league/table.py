from results.results import load_round_results
from gameweek.gameweek import get_current_round
from engine.standings import calculate_table

# =========================
# LEAGUE TABLE
# =========================

def load_table():

    ranking = calculate_table()

    table = []

    for manager, stats in ranking:

        table.append({

            "manager": manager,

            "played": (
                stats["wins"] +
                stats["draws"] +
                stats["losses"]
            ),

            "wins": stats["wins"],

            "draws": stats["draws"],

            "losses": stats["losses"],

            "gf": stats["goals_for"],

            "ga": stats["goals_against"],

            "gd": (
                stats["goals_for"] -
                stats["goals_against"]
            ),

            "points": stats["points"]

        })

    return table