import json
import os

from engine import report_templates


# ==========================================
# MEMORY FILE
# ==========================================

MEMORY_FILE = "data/report_memory.json"


# ==========================================
# LOAD MEMORY
# ==========================================

def load_memory():

    if not os.path.exists(MEMORY_FILE):

        memory = {

            "BIGGEST_WIN": -1,
            "LEADER_CHANGE": -1,
            "PLAYER_OF_ROUND": -1,
            "MANAGER_OF_ROUND": -1,
            "LEADER_STATUS": -1,

            "SUMMARY_INTRO": -1,
            "SUMMARY_ATTACK": -1,
            "SUMMARY_BALANCED": -1,
            "SUMMARY_DEFENSE": -1,

            "STREAK_WIN": -1,
            "STREAK_WITHOUT_WIN": -1,
            "TABLE_JUMP": -1

        }

        save_memory(memory)

        return memory

    with open(
        MEMORY_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ==========================================
# SAVE MEMORY
# ==========================================

def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            memory,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# GET TEMPLATE
# ==========================================

def get_template(category, **kwargs):

    templates = getattr(
        report_templates,
        category
    )

    memory = load_memory()

    index = memory.get(category, -1)

    index += 1

    if index >= len(templates):
        index = 0

    memory[category] = index

    save_memory(memory)

    return templates[index].format(**kwargs)