import json
import shutil

from pathlib import Path

from transfers.web import (
    load_manager_web
)

from gameweek.gameweek import (
    get_current_round
)


# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"


# =========================
# LINEUPS DIR
# =========================

def get_lineups_dir(manager_name):

    return (
        DATA_DIR /
        manager_name /
        "lineups"
    )


# =========================
# LINEUP FILE
# =========================

def get_lineup_file(
    manager_name,
    round_number
):

    return (
        get_lineups_dir(manager_name) /
        f"round_{round_number:02}.json"
    )


# =========================
# LOAD
# =========================

def load_lineup(
    manager_name,
    round_number
):

    file = get_lineup_file(
        manager_name,
        round_number
    )

    if not file.exists():

        return None

    with open(
        file,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# SAVE
# =========================

def save_lineup(
    manager_name,
    round_number,
    lineup
):

    folder = get_lineups_dir(
        manager_name
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    file = get_lineup_file(
        manager_name,
        round_number
    )

    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            lineup,
            f,
            ensure_ascii=False,
            indent=4
        )


# =========================
# EXISTS
# =========================

def lineup_exists(
    manager_name,
    round_number
):

    return get_lineup_file(
        manager_name,
        round_number
    ).exists()


# =========================
# COPY PREVIOUS
# =========================

def copy_previous_lineup(
    manager_name,
    round_number
):

    previous = get_lineup_file(
        manager_name,
        round_number - 1
    )

    current = get_lineup_file(
        manager_name,
        round_number
    )

    if not previous.exists():

        return False

    current.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copy(
        previous,
        current
    )

    return True


# =========================
# VALIDATE LINEUP
# =========================

def validate_lineup(
    manager_name,
    lineup
):

    manager = load_manager_web(
        manager_name
    )

    squad = manager["squad"]

    squad_names = {

        player["name"]

        for player in squad

    }

    starting = lineup["starting"]

    bench = lineup["bench"]

    formation = lineup["formation"]


    # -------------------------
    # DUPLICITY
    # -------------------------

    if len(starting) != len(set(starting)):

        return False, "V základní sestavě jsou duplicitní hráči."


    if len(bench) != len(set(bench)):

        return False, "Na lavičce jsou duplicitní hráči."


    if set(starting) & set(bench):

        return False, "Hráč nemůže být v základu i na lavičce."


    # -------------------------
    # POČET HRÁČŮ
    # -------------------------

    if len(starting) != 11:

        return False, "Základní sestava musí mít 11 hráčů."


    if len(bench) > 7:

        return False, "Na lavičce může být maximálně 7 hráčů."


    # -------------------------
    # PATŘÍ DO SOUPISKY
    # -------------------------

    for player in starting + bench:

        if player not in squad_names:

            return False, f"{player} není v soupisce manažera."


    # -------------------------
    # POČTY POZIC
    # -------------------------

    roles = {

        player["name"]: player["role"]

        for player in squad

    }

    goalkeepers = sum(

        roles[p] == "P"

        for p in starting

    )

    defenders = sum(

        roles[p] == "D"

        for p in starting

    )

    midfielders = sum(

        roles[p] == "C"

        for p in starting

    )

    forwards = sum(

        roles[p] == "A"

        for p in starting

    )


    formations = {

        "3-4-3": (3,4,3),

        "3-5-2": (3,5,2),

        "4-4-2": (4,4,2),

        "4-3-3": (4,3,3),

        "4-5-1": (4,5,1),

        "5-3-2": (5,3,2),

        "5-4-1": (5,4,1)

    }


    if formation not in formations:

        return False, "Neplatná formace."


    d, m, a = formations[formation]


    if goalkeepers != 1:

        return False, "V základní sestavě musí být právě 1 brankář."


    if defenders != d:

        return False, f"Ve formaci {formation} musí být {d} obránci."


    if midfielders != m:

        return False, f"Ve formaci {formation} musí být {m} záložníci."


    if forwards != a:

        return False, f"Ve formaci {formation} musí být {a} útočníci."


    return True, "Sestava je platná."


# =========================
# CURRENT LINEUP
# =========================

def get_current_lineup(
    manager_name
):

    round_number = get_current_round()

    lineup = load_lineup(
        manager_name,
        round_number
    )

    if lineup:

        return lineup

    copied = copy_previous_lineup(
        manager_name,
        round_number
    )

    if copied:

        return load_lineup(
            manager_name,
            round_number
        )

    # první kolo nebo zatím žádná uložená sestava
    return create_empty_lineup()


# =========================
# EXPAND LINEUP
# =========================

from serie_a.fixtures import (
    get_current_round,
    get_next_opponent
)

def expand_lineup(
    manager_name,
    lineup
):

    manager = load_manager_web(
        manager_name
    )

    squad = {

        player["name"]: player

        for player in manager["squad"]

    }

    expanded = {

        "formation": lineup["formation"],

        "starting": [],

        "bench": []

    }

    current_round = get_current_round()

    for name in lineup["starting"]:

        player = squad.get(name)

        if player is None:
            continue

        player = player.copy()

        player["fixture"] = get_next_opponent(
            player["team"],
            current_round
        )

        expanded["starting"].append(player)

    for name in lineup["bench"]:

         player = squad[name].copy()

         player["fixture"] = get_next_opponent(
             player["team"],
             current_round
         )

         expanded["bench"].append(player)

    return expanded


# =========================
# GROUP LINEUP
# =========================

def group_lineup(lineup):

    formations = {
        "3-4-3": (3, 4, 3),
        "3-5-2": (3, 5, 2),
        "4-3-3": (4, 3, 3),
        "4-4-2": (4, 4, 2),
        "4-5-1": (4, 5, 1),
        "5-3-2": (5, 3, 2),
        "5-4-1": (5, 4, 1)
    }

    d, m, a = formations[lineup["formation"]]

    grouped = {
        "goalkeeper": [],
        "defenders": [],
        "midfielders": [],
        "forwards": []
    }

    for player in lineup["starting"]:

        if player["role"] == "P":
            grouped["goalkeeper"].append(player)

        elif player["role"] == "D":
            grouped["defenders"].append(player)

        elif player["role"] == "C":
            grouped["midfielders"].append(player)

        elif player["role"] == "A":
            grouped["forwards"].append(player)

    grouped["bench"] = lineup["bench"][:]

    while len(grouped["bench"]) < 7:
        grouped["bench"].append(None)

    while len(grouped["goalkeeper"]) < 1:
        grouped["goalkeeper"].append(None)

    while len(grouped["defenders"]) < d:
        grouped["defenders"].append(None)

    while len(grouped["midfielders"]) < m:
        grouped["midfielders"].append(None)

    while len(grouped["forwards"]) < a:
        grouped["forwards"].append(None)

    grouped["formation"] = lineup["formation"]

    return grouped


# =========================
# BUILD LINEUP
# =========================

def build_lineup(
    formation,
    starting,
    bench
):

    return {

        "formation": formation,

        "starting": starting,

        "bench": bench

    }


# =========================
# EMPTY LINEUP
# =========================

def create_empty_lineup():

    return {
        "formation": "4-4-2",
        "starting": [],
        "bench": []
    }


# =========================
# SAVE CURRENT LINEUP
# =========================

def save_current_lineup(
    manager_name,
    formation,
    starting,
    bench
):

    round_number = get_current_round()

    lineup = build_lineup(
        formation,
        starting,
        bench
    )

    valid, message = validate_lineup(
        manager_name,
        lineup
    )

    if not valid:

        return False, message

    save_lineup(
        manager_name,
        round_number,
        lineup
    )

    return True, "Sestava byla uložena."


# =========================
# BUILD FROM FORM
# =========================

def build_lineup_from_form(form):

    formation = form.get("formation")

    starting = []
    bench = []

    bench_players = []

    for player_name in form:

        if player_name == "formation":
            continue

        position = form[player_name]

        if position == "starting":

            starting.append(player_name)

        elif position.startswith("bench"):

            order = int(position.replace("bench", ""))

            bench_players.append(
                (
                    order,
                    player_name
                )
            )

    bench_players.sort()

    bench = [
        player
        for _, player
        in bench_players
    ]

    return formation, starting, bench


# =========================
# REPLACE PLAYER IN CURRENT LINEUP
# =========================

def replace_player_in_current_lineup(
    manager_name,
    old_player,
    new_player
):

    round_number = get_current_round()

    lineup = load_lineup(
        manager_name,
        round_number
    )

    if lineup is None:
        return

    lineup["starting"] = [
        new_player if p == old_player else p
        for p in lineup["starting"]
    ]

    lineup["bench"] = [
        new_player if p == old_player else p
        for p in lineup["bench"]
    ]

    save_lineup(
        manager_name,
        round_number,
        lineup
    )