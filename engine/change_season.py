from engine.league_settings import set_season
from engine.reset_season import reset_current_season

from gameweek.gameweek import set_current_season


def change_season(new_season):

    set_season(new_season)

    set_current_season(new_season)

    reset_current_season()

    return True