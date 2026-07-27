import json
from pathlib import Path
from datetime import datetime


# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"

HISTORY_FILE = DATA_DIR / "player_events.json"


# =========================
# LOAD
# =========================

def load_player_history():

    if not HISTORY_FILE.exists():
        return []

    with open(
        HISTORY_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# SAVE
# =========================

def save_player_history(history):

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            ensure_ascii=False,
            indent=4
        )


# =========================
# ADD EVENT
# =========================

def add_player_event(
    player_id,
    season,
    round_number,
    event_type,
    from_manager,
    to_manager,
    transfer_type="normal",
    replaced_player_id=None
):

    history = load_player_history()

    next_id = 1

    if history:
        existing_ids = [
            item.get("id", 0)
            for item in history
        ]

        next_id = max(existing_ids) + 1

    history.append({

        "id": next_id,

        "type": event_type,

        "player_id": player_id,

        "replaced_player_id": replaced_player_id,

        "season": season,

        "round": round_number,

        "date": datetime.now().isoformat(),

        "from_manager": from_manager,

        "to_manager": to_manager,

        "transfer_type": transfer_type

    })

    save_player_history(history)


# =========================
# PLAYER HISTORY
# =========================

def get_player_history(player_id):

    history = load_player_history()

    return [

        event

        for event in history

        if event["player_id"] == player_id

    ]