import json
import os


# =========================
# FILE
# =========================

FILE = "data/records.json"


# =========================
# LOAD
# =========================

def load_records():

    if not os.path.exists(FILE):

        return {

            "highest_score": {
                "manager": "",
                "value": 0
            },

            "most_goals": {
                "manager": "",
                "value": 0
            },

            "biggest_win": {
                "match": "",
                "difference": 0
            },

            "best_average": {
                "manager": "",
                "value": 0
            }

        }

    with open(FILE, encoding="utf-8") as f:

        return json.load(f)


# =========================
# SAVE
# =========================

def save_records(records):

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            records,
            f,
            ensure_ascii=False,
            indent=4
        )


# =========================
# PRINT
# =========================

def print_records(records):

    print("\n========================================")
    print("LEAGUE RECORDS")
    print("========================================\n")

    print(
        f"🔥 Nejvyšší skóre:\n"
        f"{records['highest_score']['manager']} "
        f"({records['highest_score']['value']})\n"
    )

    print(
        f"⚽ Nejvíce gólů:\n"
        f"{records['most_goals']['manager']} "
        f"({records['most_goals']['value']})\n"
    )

    print(
        f"💥 Největší výhra:\n"
        f"{records['biggest_win']['match']} "
        f"({records['biggest_win']['difference']} gólů)\n"
    )

    print(
        f"📈 Nejlepší průměr:\n"
        f"{records['best_average']['manager']} "
        f"({records['best_average']['value']})"
    )