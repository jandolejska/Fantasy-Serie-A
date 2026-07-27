from gameweek.gameweek import (
    open_new_round,
    set_lineup_locked
)


# =========================
# OPEN NEW ROUND
# =========================

def admin_open_new_round(deadline):

    return open_new_round(deadline)


# =========================
# LOCK LINEUPS
# =========================

def admin_lock_lineups():

    set_lineup_locked(
        True
    )


# =========================
# UNLOCK LINEUPS
# =========================

def admin_unlock_lineups():

    set_lineup_locked(
        False
    )