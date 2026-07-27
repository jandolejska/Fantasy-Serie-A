# =========================
# MANAGER OF ROUND
# =========================

def manager_of_round(results):

    best = None

    for match in results:

        candidates = [

            (match["home"], match["home_score"]),
            (match["away"], match["away_score"])

        ]

        for manager, score in candidates:

            if best is None or score > best["score"]:

                best = {
                    "manager": manager,
                    "score": score
                }

    return best


def print_manager_award(round_number, results):

    winner = manager_of_round(results)

    print("\n========================================")
    print(f"MANAGER OF ROUND {round_number}")
    print("========================================")
    print(
        f"🏆 {winner['manager']} "
        f"({winner['score']} bodů)"
    )
    
    return winner

# =========================
# PLAYER OF ROUND
# =========================

def player_of_round(players):

    best = None

    for player in players:

        if player["grade"] is None:
            continue

        grade = float(
            str(player["grade"]).replace(",", ".")
        )

        if best is None or grade > best["grade"]:

            best = {
                "name": player["name"],
                "team": player["team"],
                "grade": grade
            }

    return best


def print_player_award(round_number, players):

    winner = player_of_round(players)

    print("\n========================================")
    print(f"PLAYER OF ROUND {round_number}")
    print("========================================")
    print(f"⭐ {winner['name']}")
    print(f"{winner['team']}")
    print(f"Známka: {winner['grade']}")

    return winner

# =========================
# TEAM OF ROUND
# =========================

def team_of_round(players):

    goalkeepers = []
    defenders = []
    midfielders = []
    attackers = []

    for player in players:

        grade = float(
            str(player["grade"]).replace(",", ".")
        )

        player_data = {
            "name": player["name"],
            "grade": grade
        }

        if player["role"] == "P":
            goalkeepers.append(player_data)

        elif player["role"] == "D":
            defenders.append(player_data)

        elif player["role"] == "C":
            midfielders.append(player_data)

        elif player["role"] == "A":
            attackers.append(player_data)

    goalkeepers.sort(
        key=lambda x: x["grade"],
        reverse=True
    )

    defenders.sort(
        key=lambda x: x["grade"],
        reverse=True
    )

    midfielders.sort(
        key=lambda x: x["grade"],
        reverse=True
    )

    attackers.sort(
        key=lambda x: x["grade"],
        reverse=True
    )

    return (
        goalkeepers[:1]
        + defenders[:4]
        + midfielders[:3]
        + attackers[:3]
    )


def print_team_of_round(players):

    team = team_of_round(players)

    print("\n========================================")
    print("TEAM OF THE ROUND")
    print("========================================")

    for player in team:

        print(
            f"{player['name']:<20}"
            f"{player['grade']}"
        )

    return team