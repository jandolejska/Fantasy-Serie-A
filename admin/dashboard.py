from pathlib import Path

from transfers.web import (
    load_managers
)

from gameweek.gameweek import (
    get_current_round,
    get_completed_rounds,
    get_deadline,
    is_lineup_locked,
    load_fixtures
)


# =========================
# ADMIN DASHBOARD
# =========================

def load_admin_dashboard():

    managers = load_managers()

    fixtures = load_fixtures()

    total_rounds = len(fixtures)

    current_round = get_current_round()

    locked = is_lineup_locked()

    played_rounds = get_completed_rounds()

    remaining_rounds = max(
        0,
        total_rounds - played_rounds
    )

    round_played = (
        played_rounds >= current_round
    )

    season_finished = (
        current_round >= total_rounds
        and round_played
    )

    if season_finished:

        status = "🏆 Sezóna dokončena"
        next_step = "-"

    elif round_played:

        status = "🏁 Kolo odehráno"
        next_step = "📅 Otevřít nové kolo"

    elif not locked:

        status = "🟢 Kolo otevřeno"
        next_step = "🔒 Uzamknout sestavy"

    else:

        status = "🔒 Sestavy uzamčeny"
        next_step = "📥 Import známek a odehrát kolo"

    return {

        "gameweek": current_round,

        "total_rounds": total_rounds,

        "played_rounds": played_rounds,

        "remaining_rounds": remaining_rounds,

        "deadline": get_deadline(),

        "locked": locked,

        "round_played": round_played,

        "season_finished": season_finished,

        "status": status,

        "managers": len(managers),

        "next_step": next_step

    }