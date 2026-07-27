from flask import render_template

from players.profile import load_player_profile
 

def player_route(player_id):

    profile = load_player_profile(player_id)

    if profile is None:
        return "Hráč nenalezen.", 404

    return render_template(
        "player.html",
        player=profile["player"],
        owner=profile["owner"],
        grades=profile["grades"],
        stats=profile["stats"],
        history=profile["history"],
        active_page="league"
    )