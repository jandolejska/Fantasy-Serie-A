from transfers.manager import (
    replace_player,
    save_manager
)

from transfers.budget import (
    can_buy_player
)

from transfers.database import (
    get_current_price
)

from transfers.database import (
    load_players,
    available_players,
    filter_role
)

from transfers.web import (
    load_manager_web,
    load_managers,
    load_coaches
)

from lineups.lineup import (
    replace_player_in_current_lineup
)

from serie_a.teams import get_team
from news.news import add_news
from coaches.coaches import load_coaches
from history.player_history import add_player_event


# =========================
# AVAILABLE COACHES
# =========================

def available_coaches(manager):

    coaches = load_coaches()

    managers = load_managers()

    used_coaches = {
        m["coach"]
        for m in managers
        if m["slug"] != manager["slug"]
    }

    return [
        coach
        for coach in coaches
        if coach not in used_coaches
    ]


# =========================
# LOAD SQUAD
# =========================

def load_squad(manager_name):

    manager = load_manager_web(
        manager_name
    )

    grouped = {

        "goalkeeper": [],

        "defenders": [],

        "midfielders": [],

        "forwards": []

    }

    for player in manager["squad"]:

        if player["role"] == "P":

            grouped["goalkeeper"].append(
                player
            )

        elif player["role"] == "D":

            grouped["defenders"].append(
                player
            )

        elif player["role"] == "C":

            grouped["midfielders"].append(
                player
            )

        elif player["role"] == "A":

            grouped["forwards"].append(
                player
            )

    return grouped


# =========================
# MAKE TRANSFER
# =========================

def make_transfer(
    manager,
    sold_player,
    bought_player
):

    sell_price = sold_player.get(
        "buy_price",
        0
    )

    buy_price = get_current_price(
        bought_player
    )

    if not can_buy_player(
        manager,
        sell_price,
        buy_price
    ):

        return (
            False,
            "❌ Nedostatek budgetu."
        )

    if manager["transfers_left"] <= 0:

        return (
            False,
            "❌ Nemáš žádné přestupy."
        )

    new_player = bought_player.copy()

    new_player["buy_price"] = buy_price

    replaced = replace_player(
        manager,
        sold_player,
        new_player
    )

    replace_player_in_current_lineup(
        manager["slug"],
        sold_player["name"],
        new_player["name"]
    )

    if not replaced:

        return (
            False,
            "❌ Hráč nebyl nalezen v soupisce."
        )

    manager["budget"] += sell_price

    manager["budget"] -= buy_price

    manager["transfers_left"] -= 1

    save_manager(manager)

    add_player_event(
        player_id=bought_player["id"],
        replaced_player_id=sold_player["id"],
        season=1,
        round_number=1,
        event_type="transfer",
        from_manager=None,
        to_manager=manager["name"],
        transfer_type="normal"
    )

    add_news(
        {
            "type": "normal",
            "manager": manager["name"],
            "sold": {
                "name": sold_player["name"],
                "team": sold_player["team"]
            },
            "bought": {
                "name": bought_player["name"],
                "team": bought_player["team"]
            }
        }
    )

    return (
        True,
        "✅ Přestup byl úspěšně proveden."
    )


# =========================
# MAKE FREE TRANSFER
# =========================

def make_free_transfer(
    manager,
    sold_player,
    bought_player
):

    sell_price = sold_player.get(
        "buy_price",
        0
    )

    buy_price = get_current_price(
        bought_player
    )

    if not can_buy_player(
        manager,
        sell_price,
        buy_price
    ):

        return (
            False,
            "❌ Nedostatek budgetu."
        )

    new_player = {

        "name": bought_player["name"],
        "role": bought_player["role"],
        "buy_price": buy_price

    }

    replaced = replace_player(
        manager,
        sold_player,
        new_player
    )

    replace_player_in_current_lineup(
        manager["slug"],
        sold_player["name"],
        new_player["name"]
    )

    if not replaced:

        return (
            False,
            "❌ Hráč nebyl nalezen."
        )

    # Uprav budget stejně jako u klasického přestupu
    manager["budget"] += sell_price
    manager["budget"] -= buy_price

    # Jen NEODEČÍTEJ manager["transfers_left"]

    save_manager(manager)

    add_player_event(
        player_id=bought_player["id"],
        replaced_player_id=sold_player["id"],
        season=1,
        round_number=1,
        event_type="transfer",
        from_manager=None,
        to_manager=manager["name"],
        transfer_type="free"
    )

    add_news(
        {
            "type": "free",
            "manager": manager["name"],
            "sold": {
                "name": sold_player["name"],
                "team": sold_player["team"]
            },
            "bought": {
                "name": bought_player["name"],
                "team": bought_player["team"]
            }
        }
    )

    return (
        True,
        "✅ Free transfer byl úspěšně proveden."
    )


# =========================
# COACH TRANSFER
# =========================

def make_coach_transfer(
    manager_slug,
    new_coach
):

    manager = load_manager_web(
        manager_slug
    )

    if manager is None:

        return (
            False,
            "Manažer nebyl nalezen."
        )

    if manager["coach"] == new_coach:

        return (
            False,
            "Tento trenér je již vybrán."
        )

    old_coach = manager["coach"]

    coaches = load_coaches()

    old_team = coaches.get(old_coach, {}).get("team")
    new_team = coaches.get(new_coach, {}).get("team")

    manager["coach"] = new_coach

    save_manager(manager)

    add_news(
        {
            "type": "coach",
            "manager": manager["name"],
            "old": old_coach,
            "old_team": old_team,
            "new": new_coach,
            "new_team": new_team
        }
    )

    return (
        True,
        f"Trenér změněn na {new_coach}."
    )


# =========================
# FIND PLAYER
# =========================

def find_player(manager_name, player_name):

    manager = load_manager_web(
        manager_name
    )

    for player in manager["squad"]:

        if player["name"] == player_name:

            return player

    return None


# =========================
# AVAILABLE REPLACEMENTS
# =========================

def load_available_replacements(
    manager,
    sold_player
):

    players = load_players()

    players = available_players(
        players,
        manager
    )

    players = filter_role(
        players,
        sold_player["role"]
    )

    players.sort(
        key=lambda x: x["qa"]
    )

    for player in players:

        player["team_info"] = get_team(
            player["team"]
        )

    return players