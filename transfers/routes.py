from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from transfers.web import (
    load_manager_web
)

from transfers.transfers import (
    load_squad,
    find_player,
    load_available_replacements,
    available_coaches,
    make_transfer,
    make_free_transfer,
    make_coach_transfer
)


# ==================================================
# PLAYER POST
# ==================================================

def handle_player_post(
    manager,
    manager_name,
    transfer_type
):

    sold_name = request.form.get(
        "sold"
    )

    buy_name = request.form.get(
        "buy"
    )

    sold_player = find_player(
        manager_name,
        sold_name
    )

    if sold_player is None:

        flash(
            "Prodávaný hráč nebyl nalezen.",
            "danger"
        )

        return redirect(
            url_for(
                "transfers",
                type=transfer_type
            )
        )

    available = load_available_replacements(
        manager,
        sold_player
    )

    bought_player = None

    for player in available:

        if player["name"] == buy_name:

            bought_player = player

            break

    if bought_player is None:

        flash(
            "Kupovaný hráč nebyl nalezen.",
            "danger"
        )

        return redirect(
            url_for(
                "transfers",
                type=transfer_type
            )
        )

    if transfer_type == "free":

        success, message = make_free_transfer(
            manager,
            sold_player,
            bought_player
        )

    else:

        success, message = make_transfer(
            manager,
            sold_player,
            bought_player
        )

    flash(
        message,
        "success" if success else "danger"
    )

    return redirect(
        url_for(
            "transfers",
            type=transfer_type
        )
    )


# ==================================================
# COACH POST
# ==================================================

def handle_coach_post(
    manager_name
):

    new_coach = request.form.get(
        "coach"
    )

    success, message = make_coach_transfer(
        manager_name,
        new_coach
    )

    flash(
        message,
        "success" if success else "danger"
    )

    return redirect(
        url_for(
            "transfers",
            type="coach"
        )
    )


# ==================================================
# TRANSFERS ROUTE
# ==================================================

def transfers_route():

    if "username" not in session:

        return redirect(
            url_for("login")
        )

    if session["role"] != "manager":

        return redirect(
            url_for("index")
        )

    manager_name = session["manager"].lower()

    manager = load_manager_web(
        manager_name
    )

    transfer_type = request.args.get(
        "type",
        "normal"
    )

    transfer_type = request.form.get(
        "transfer_type",
        transfer_type
    )

    squad = load_squad(
        manager_name
    )

    coach_list = []

    if transfer_type == "coach":

        coach_list = available_coaches(
            manager
        )

    # ==========================================
    # POST
    # ==========================================

    if request.method == "POST":

        if transfer_type == "coach":

            return handle_coach_post(
                manager_name
            )

        return handle_player_post(
            manager,
            manager_name,
            transfer_type
        )

    # ==========================================
    # GET
    # ==========================================

    sold_player = request.args.get(
        "sell"
    )

    bought_player = request.args.get(
        "buy"
    )

    selected_player = None

    budget_after_sale = None

    available_players = []

    if sold_player:

        selected_player = find_player(
            manager_name,
            sold_player
        )

        if selected_player:

            budget_after_sale = (

                manager["budget"]

                + selected_player["buy_price"]

            )

            available_players = load_available_replacements(
                manager,
                selected_player
            )

    selected_buy = None

    budget_after_transfer = None

    if bought_player:

        for player in available_players:

            if player["name"] == bought_player:

                selected_buy = player

                budget_after_transfer = (

                    budget_after_sale

                    - player["qa"]

                )

                break

    role_title = "Hráči"

    if selected_player:

        if selected_player["role"] == "P":

            role_title = "🥅 Dostupní brankáři"

        elif selected_player["role"] == "D":

            role_title = "🛡 Dostupní obránci"

        elif selected_player["role"] == "C":

            role_title = "🎯 Dostupní záložníci"

        elif selected_player["role"] == "A":

            role_title = "⚽ Dostupní útočníci"

    if transfer_type == "coach":

        subtitle = "Vyber nového trenéra."

    else:

        subtitle = "Vyber hráče, kterého chceš prodat."

        if selected_player:

            subtitle = (
                f"Vyber náhradu za "
                f"{selected_player['name']}."
            )

        if selected_buy:

           subtitle = (
                "Zkontroluj přestup "
                "a potvrď ho."
            )

    return render_template(

        "transfers.html",

        manager=manager,

        squad=squad,

        transfer_type=transfer_type,

        coach_list=coach_list,

        sold_player=sold_player,

        selected_player=selected_player,

        budget_after_sale=budget_after_sale,

        selected_buy=selected_buy,

        budget_after_transfer=budget_after_transfer,

        role_title=role_title,

        subtitle=subtitle,

        active_page="transfers",

        available_players=available_players

    )