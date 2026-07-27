def print_hall_of_fame(table):

    print("\n========================================")
    print("HALL OF FAME")
    print("========================================\n")

    champion = table[0]

    print("🏆 Champion")
    print(champion["team"])

    print()

    best_attack = max(
        table,
        key=lambda x: x["gf"]
    )

    print("⚽ Best Attack")
    print(f"{best_attack['team']} ({best_attack['gf']} gólů)")

    print()

    best_defence = min(
        table,
        key=lambda x: x["ga"]
    )

    print("🛡 Best Defence")
    print(f"{best_defence['team']} ({best_defence['ga']} inkasovaných)")