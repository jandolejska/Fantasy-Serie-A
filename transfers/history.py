import json
from pathlib import Path
from datetime import datetime


# =========================
# PATH
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"


# =========================
# HISTORY FILE
# =========================

def get_history_file(manager_name):

    return (
        DATA_DIR /
        manager_name /
        "transfers.json"
    )


# =========================
# LOAD HISTORY
# =========================

def load_history(manager_name):

    file = get_history_file(
        manager_name
    )

    if not file.exists():

        return []

    with open(
        file,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# SAVE HISTORY
# =========================

def save_history(
    manager_name,
    history
):

    file = get_history_file(
        manager_name
    )

    with open(
        file,
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
# ADD TRANSFER
# =========================

def add_transfer(
    manager_name,
    sold_player,
    bought_player,
    sell_price,
    buy_price,
    transfers_left,
    free_transfer=False
):

    history = load_history(
        manager_name
    )

    history.append({

        "date": datetime.now().strftime(
        "%d.%m.%Y %H:%M"
        ),

        "type": (
            "FREE_TRANSFER"
            if free_transfer
            else "TRANSFER"
        ),

        "out": sold_player,

        "in": bought_player,

        "sell_price": sell_price,

        "buy_price": buy_price,

        "difference": sell_price - buy_price,

        "transfers_left": transfers_left

    })

    save_history(
        manager_name,
        history
    )