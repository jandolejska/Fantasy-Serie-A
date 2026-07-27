# =========================
# AUTOMATIC SUBSTITUTIONS
# =========================

def make_substitutions(starting, bench):

    final_team = []

    substitutions = []

    # projdeme základní sestavu
    for starter in starting:

        # hráč má známku → zůstává
        if starter["grade"] is not None:
            final_team.append(starter)
            continue

        # hledáme náhradníka stejného postu
        substitute = None

        for reserve in bench:

            if reserve["role"] != starter["role"]:
                continue

            if reserve["grade"] is None:
                continue

            substitute = reserve
            break

        # pokud jsme našli náhradníka
        if substitute:

            replacement = substitute.copy()
            replacement["replaced_player"] = starter

            final_team.append(replacement)

            substitutions.append({
                "out": starter,
                "in": substitute
            })

            bench.remove(substitute)

        # jinak tým hraje o hráče méně
        else:
            final_team.append(starter)

    return final_team, substitutions