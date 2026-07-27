from engine.manager import build_team
from engine.calculator import calculate_team_score, score_to_goals
from engine.substitution import make_substitutions


def play_manager(manager_name, round_number, players, home=False):

    # načtení manažera a sestavy
    manager, starting, bench = build_team(
        manager_name,
        round_number,
        players
    )

    # automatické střídání
    starting, substitutions = make_substitutions(
        starting,
        bench
    )

    # výpočet bodů (bonus trenéra se přidává až v league.py)
    score = calculate_team_score(
        starting,
        home=home,
        coach_bonus=0
    )

    goals = score_to_goals(score)

    return {
        "manager": manager,
        "starting": starting,
        "bench": bench,
        "substitutions": substitutions,
        "score": score,
        "goals": goals
    }