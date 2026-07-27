from gameweek.gameweek import (
    load_gameweek,
    is_lineup_locked,
    get_completed_rounds
)

from league.table import (
    load_table
)

from engine.results import load_last_round

from gameweek.gameweek import (
    load_gameweek,
    is_lineup_locked,
    get_next_round_fixtures
)

from news.news import (
    load_news
)

from serie_a.teams import load_teams

# =========================
# DASHBOARD
# =========================

def load_dashboard(manager):

    gameweek = load_gameweek()

    news = load_news()

    teams = load_teams()

    last = load_last_round()
    next_round = get_next_round_fixtures()

    print("LAST:", last)
    print("NEXT:", next_round)

    dashboard = {

        "manager": manager,

        "current_round": gameweek["current_round"],

        "deadline": gameweek["deadline"],

        "locked": is_lineup_locked(),

        "last_results": last,

        "table": load_table(),

        "completed_rounds": get_completed_rounds(),

        "next_round": next_round,

        "news": news,

        "teams": teams

    }

    return dashboard