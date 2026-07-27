# =========================
# BUDGET LIMIT
# =========================

BUDGET_LIMIT = 333


# =========================
# SPENT MONEY
# =========================

def get_spent_budget(manager):

    spent = 0

    for player in manager["squad"]:

        spent += player.get(
            "buy_price",
            0
        )

    return spent


# =========================
# FREE BUDGET
# =========================

def get_free_budget(manager):

    spent = get_spent_budget(
        manager
    )

    return BUDGET_LIMIT - spent


# =========================
# CAN BUY PLAYER
# =========================

def can_buy_player(
    manager,
    sell_price,
    buy_price
):

    free_budget = get_free_budget(
        manager
    )

    available = (
        free_budget +
        sell_price
    )

    return available >= buy_price


# =========================
# PRINT BUDGET
# =========================

def print_budget(manager):

    spent = get_spent_budget(
        manager
    )

    free = get_free_budget(
        manager
    )

    print()

    print("=" * 40)
    print("BUDGET")
    print("=" * 40)

    print(f"Utraceno: {spent}")
    print(f"Limit: {BUDGET_LIMIT}")
    print(f"Volno: {free}")

    print()