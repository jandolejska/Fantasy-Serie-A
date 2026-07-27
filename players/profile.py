from datetime import datetime

from players.service import (
    get_player,
    get_player_owner
)

from players.grades import load_player_grades
from history.player_history import get_player_history


def load_player_profile(player_id):
    """
    Načte kompletní profil hráče.

    Zatím obsahuje pouze základní informace.
    Další části (známky, statistiky, historie...)
    budeme postupně přidávat.
    """

    player = get_player(player_id)

    if player is None:
        return None

    owner = get_player_owner(player_id)

    history = get_player_history(player_id)

    # Formátování data pro zobrazení
    for event in history:

        if event.get("date"):

            try:

                event["date_formatted"] = datetime.fromisoformat(
                    event["date"]
                ).strftime("%d.%m.%Y %H:%M")

            except Exception:

                event["date_formatted"] = event["date"]

    return {

        "player": player,

        "owner": owner,

        "grades": load_player_grades(player_id),

        "stats": {},

        "history": history

    }