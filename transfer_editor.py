from transfers.manager import (
    get_manager_names,
    load_manager,
    save_manager,
    find_player
)

from transfers.database import (
    load_players,
    available_players,
    filter_role,
    get_current_price
)

from transfers.budget import (
    print_budget
)

from transfers.transfer import (
    make_transfer,
    make_free_transfer
)

from transfers.database import (
    search_players
)

from transfers.restore import (
    list_backups,
    restore_backup
)

from transfers.league_stats import (
    print_league
)

from transfers.coach import load_coaches
from transfers.ownership import get_owned_coaches
from transfers.history import add_transfer
from transfers.backup import create_backup

# =========================
# CHOOSE MANAGER
# =========================

def choose_manager():

    managers = get_manager_names()

    print("=" * 40)
    print("TRANSFER EDITOR")
    print("=" * 40)
    print()

    for i, manager in enumerate(
        managers,
        start=1
    ):

        print(f"{i}. {manager}")

    print()

    choice = int(input("> "))

    return managers[
        choice - 1
    ]


# =========================
# PRINT SQUAD
# =========================

def print_squad(manager):

    print()
    print("=" * 40)
    print(manager["name"])
    print("=" * 40)

    print()

    print(f"Trenér: {manager['coach']}")

    print_budget(manager)

    print(
        f"Přestupy: "
        f"{manager['transfers_left']}"
    )

    print()

    for i, player in enumerate(
        manager["squad"],
        start=1
    ):

        print(
            f"{i:>2}. "
            f"{player['name']:<22}"
            f"{player['role']} "
            f"{player.get('buy_price', '-')}"
        )


# =========================
# CHOOSE PLAYER TO SELL
# =========================

def choose_player(manager):

    print()
    print("=" * 40)
    print("PRODEJ HRÁČE")
    print("=" * 40)
    print()

    for i, player in enumerate(
        manager["squad"],
        start=1
    ):

        print(
            f"{i:>2}. "
            f"{player['name']:<22}"
            f"{player['role']} "
            f"{player.get('buy_price', '-')}"
        )

    print()

    choice = int(input("> "))

    return manager["squad"][choice - 1]


# =========================
# CHOOSE PLAYER TO BUY
# =========================

def choose_new_player(
    players,
    manager,
    role
):
    available = available_players(
        players,
        manager
    )

    available = filter_role(
        available,
        role
    )

    while True:

        print()
        print("=" * 40)
        print("HLEDÁNÍ HRÁČE")
        print("=" * 40)

        search = input(
            "\nZadej část jména: "
        )

        results = search_players(
            available,
            search,
            role
        )

        if len(results) == 0:

            print("\nNikdo nenalezen.")
            continue

        print()

        for i, player in enumerate(
            results,
            start=1
        ):

            print(
                f"{i}. "
                f"{player['name']:<22}"
                f"{player['team']:<18}"
                f"{player['qa']}"
            )

        print()

        choice = int(input("> "))

        return results[
            choice - 1
        ]


# =========================
# CHOOSE NEW COACH
# =========================

from transfers.coach import load_coaches


def choose_new_coach(manager):

    coaches = load_coaches()

    owned = get_owned_coaches()

    available = []

    for coach in coaches:

        if coach == manager["coach"]:
            continue

        if coach in owned:
           continue

        available.append(coach)

    print()
    print("=" * 40)
    print("VÝMĚNA TRENÉRA")
    print("=" * 40)
    print()

    print(f"Aktuální trenér: {manager['coach']}")
    print()

    for i, coach in enumerate(
        available,
        start=1
    ):

        print(f"{i}. {coach}")

    print()

    choice = int(input("> "))

    return available[
        choice - 1
    ]


# =========================
# RESTORE BACKUP
# =========================

def restore_manager_backup(manager):

    backups = list_backups(
        manager["name"]
    )

    if len(backups) == 0:

        print()
        print("Žádné zálohy nebyly nalezeny.")
        return

    print()
    print("=" * 40)
    print("OBNOVA ZÁLOHY")
    print("=" * 40)
    print()

    for i, backup in enumerate(
        backups,
        start=1
    ):

        print(
            f"{i}. {backup.stem}"
        )

    print()

    choice = int(input("> "))

    backup = backups[
        choice - 1
    ]

    print()
    print(
        f"Vybraná záloha: {backup.stem}"
    )

    answer = input(
        "Obnovit? (a/n): "
    )

    if answer.lower() != "a":

        print()
        print("Obnova zrušena.")
        return

    create_backup(
        manager["name"]
    )

    restore_backup(
        manager["name"],
        backup
    )

    print()
    print("✅ Záloha byla obnovena.")


# =========================
# CHOOSE FREE TRANSFER
# =========================

def choose_free_player(
    manager,
    players
):

    candidates = []

    for squad_player in manager["squad"]:

        for player in players:

            if player["name"] != squad_player["name"]:
                continue

            if not player["active"]:

                candidates.append(
                    squad_player
                )

            break

    if len(candidates) == 0:

        print()
        print("Žádný hráč není dostupný pro Free Transfer.")

        return None

    print()
    print("=" * 40)
    print("FREE TRANSFER")
    print("=" * 40)
    print()

    for i, player in enumerate(
        candidates,
        start=1
    ):

        print(
            f"{i}. "
            f"{player['name']:<22}"
            f"{player['role']}  "
            f"{player['buy_price']}"
        )

    print()

    choice = int(input("> "))

    return candidates[
        choice - 1
    ]
# =========================
# CONFIRM TRANSFER
# =========================

def confirm_transfer(
    manager,
    sold_player,
    bought_player,
    free_transfer=False
):

    sell_price = sold_player["buy_price"]
    buy_price = get_current_price(
        bought_player
    )

    print()

    print("=" * 40)

    if free_transfer:
        print("POTVRZENÍ FREE TRANSFERU")
    else:
        print("POTVRZENÍ PŘESTUPU")

    print("=" * 40)

    print()

    print(
        f"Prodáváš : "
        f"{sold_player['name']}"
    )

    print(
        f"Kupuješ  : "
        f"{bought_player['name']}"
    )

    print()

    print(f"Prodejní cena : {sell_price}")
    print(f"Nákupní cena  : {buy_price}")

    difference = buy_price - sell_price

    if difference >= 0:

        print(
            f"Doplatek      : +{difference}"
        )

    else:

        print(
            f"Zisk          : {-difference}"
        )

    print()

    answer = input(
        "Potvrdit přestup? (a/n): "
    )

    return answer.lower() == "a"


# =========================
# PRINT MENU
# =========================

def print_menu():

    print()
    print("=" * 40)
    print("MENU")
    print("=" * 40)

    print("1. Přestup hráče")
    print("2. Free transfer")
    print("3. Výměna trenéra")
    print("4. Zobraz soupisku")
    print("5. Budget")
    print("6. Obnovit zálohu")
    print("7. Statistiky ligy")
    print("8. Konec")

    print()

    return input("> ")


# =========================
# MAIN MENU
# =========================

def menu():

    players = load_players()

    manager_name = choose_manager()

    manager = load_manager(
        manager_name
    )

    while True:

        choice = print_menu()

        if choice == "1":

            sold_player = choose_player(
                manager
            )

            bought_player = choose_new_player(
                players,
                manager,
                sold_player["role"]
            )

            if not confirm_transfer(
                manager,
                sold_player,
                bought_player
            ):

                print("\nPřestup zrušen.")
                continue

            success, message = make_transfer(
                manager,
                sold_player,
                bought_player
            )

            print()
            print(message)

            if success:

                create_backup(
                    manager["name"]
                )

                save_manager(manager)

                add_transfer(

                    manager["name"],

                    sold_player["name"],

                    bought_player["name"],

                    sold_player["buy_price"],

                    bought_player["qa"],

                    manager["transfers_left"]

                )

                print_budget(manager)

        elif choice == "2":

            sold_player = choose_free_player(
                manager,
                players
            )

            if sold_player is None:
                continue

            bought_player = choose_new_player(
                players,
                manager,
                sold_player["role"]
            )

            if not confirm_transfer(
                manager,
                sold_player,
                bought_player,
                free_transfer=True
            ):

                print("\nFree transfer zrušen.")
                continue

            success, message = make_free_transfer(
                manager,
                sold_player,
                bought_player
            )

            print()
            print(message)

            if success:

                create_backup(
                    manager["name"]
                )

                save_manager(manager)

                add_transfer(

                    manager["name"],

                    sold_player["name"],

                    bought_player["name"],

                    sold_player["buy_price"],

                    bought_player["qa"],

                    manager["transfers_left"],

                    free_transfer=True

                )

                print_budget(manager)

        elif choice == "3":

            new_coach = choose_new_coach(
                manager
            )

            print()

            print(
                f"{manager['coach']} → {new_coach}"
            )

            answer = input(
                "Potvrdit změnu? (a/n): "
            )

            if answer.lower() == "a":

                create_backup(
                    manager["name"]
                )

                manager["coach"] = new_coach

                save_manager(manager)

                print()
                print("✅ Trenér změněn.")

            else:

                print()
                print("Změna zrušena.")

        elif choice == "4":

            print_squad(manager)

        elif choice == "5":

            print_budget(manager)

        elif choice == "6":

            restore_manager_backup(
                manager
            )

            manager = load_manager(
                manager["name"]
            )

        elif choice == "7":

            print_league()

        elif choice == "8":

            print("\nEditor ukončen.")
            break

        else:

            print("\nNeplatná volba.")


# =========================
# START
# =========================

if __name__ == "__main__":

    menu()