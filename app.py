import os

from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from transfers.web import (
    load_managers,
    load_manager_web,
    get_league_summary
)

from web.auth import (
    authenticate
)

from web.display import (
    display_name
)

from web.league import (
    get_standings,
    get_season
)

from lineups.lineup import (
    get_current_lineup,
    expand_lineup,
    group_lineup,
    save_current_lineup,
    build_lineup_from_form
)

from gameweek.gameweek import (
    is_lineup_locked,
    open_new_round,
    set_lineup_locked,
    auto_lock_lineups
)

from dashboard.dashboard import (
    load_dashboard
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

from admin.dashboard import (
    load_admin_dashboard
)

from admin.gameweek import (
    admin_open_new_round,
    admin_lock_lineups,
    admin_unlock_lineups
)

from engine.import_grades import (
    import_grades
)

from flask import flash
from engine.league import play_current_round
from engine.standings import calculate_table
from league.table import load_table
from engine.report import load_report
from engine.results import (
    load_all_rounds,
    load_round,
    load_fixture
)

from gameweek.fixtures import (
    load_round_fixtures
)

from transfers.routes import (
    transfers_route
)

from players.routes import player_route

from datetime import timedelta

from engine.import_draft import import_draft

from engine.reset_season import reset_current_season

from engine.change_season import change_season

load_dotenv()

app = Flask(__name__)

@app.before_request
def check_deadline():

    auto_lock_lineups()

app.jinja_env.globals["display_name"] = display_name

app.config.from_object("config.Config")


# =========================
# HOME
# =========================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def index():

    if request.method == "POST":

        action = request.form.get(
            "action"
        )

        if action == "new_round":

            deadline = request.form.get(
                "deadline"
            )

            print("DEADLINE:", deadline)

            if admin_open_new_round(
                deadline
            ):

               flash(
                   "✅ Nové kolo bylo otevřeno.",
                   "success"
               )

            else:

               flash(
                   "🏁 Sezóna už skončila. Další kolo nelze otevřít.",
                   "warning"
               )

            return redirect(
                url_for("index")
            )

        elif action == "lock":

            admin_lock_lineups()

            flash(
                "🔒 Sestavy byly uzamčeny.",
                "success"
            )

            return redirect(
                url_for("index")
            )

        elif action == "unlock":

            admin_unlock_lineups()

            flash(
                "🔓 Sestavy byly odemčeny.",
                "success"
            )

            return redirect(
                url_for("index")
            )

        elif action == "download_grades":

            player_count, coach_count = import_grades()

            flash(
                f"✅ Import dokončen. Importováno {player_count} hráčů a {coach_count} trenérů.",
                "success"
            )

            return redirect(
                url_for("index")
            )

        elif action == "import_draft":

            file = request.files.get("draft_file")

            if not file or file.filename == "":

                flash(
                    "❌ Nebyl vybrán žádný soubor.",
                    "danger"
                )

                return redirect(url_for("index"))

            upload_path = "Draft.xlsx"

            file.save(upload_path)

            try:

                report = import_draft(upload_path)

                flash(
                    "✅ Draft byl úspěšně importován.",
                    "success"
                )

                for row in report:

                    flash(
                        f"{row['manager']}: "
                        f"{row['players']} hráčů | "
                        f"{row['coach']} | "
                        f"{row['budget']} M",
                        "info"
                    )

            except Exception as e:

                flash(
                    str(e),
                    "danger"
                )

            return redirect(url_for("index"))

        elif action == "reset_current_season":

            try:

                reset_current_season()

                flash(
                    "🔄 Aktuální sezóna byla úspěšně resetována.",
                    "success"
                )

            except Exception as e:

                flash(
                    str(e),
                    "danger"
                )

            return redirect(
                url_for("index")
            )

        elif action == "change_season":

            new_season = request.form.get("new_season")

            if not new_season:

                flash(
                    "❌ Zadejte název nové sezóny.",
                    "danger"
                )

                return redirect(url_for("index"))

            try:

                change_season(new_season)

                flash(
                    f"🏁 Nová sezóna {new_season} byla úspěšně zahájena.",
                    "success"
                )

            except Exception as e:

                flash(
                    str(e),
                    "danger"
                )

            return redirect(url_for("index"))

        elif action == "play_round":

            played, manager = play_current_round()

            if played:

                flash(
                    "✅ Kolo bylo úspěšně odehráno.",
                    "success"
                )

            else:

                if manager:

                    flash(
                        f"❌ Manažer {manager} nemá uloženou sestavu pro aktuální kolo.",
                        "danger"
                    )

                else:

                    flash(
                        "❌ Aktuální kolo nebylo nalezeno v rozpisu.",
                        "danger"
                    )

            return redirect(url_for("index"))

    if "username" not in session:

        return redirect(
            url_for("login")
        )

    if session["role"] == "admin":

        dashboard = load_admin_dashboard()

        return render_template(

            "admin/dashboard.html",

            dashboard=dashboard

        )

    if session["role"] == "manager":

        manager = load_manager_web(
            session["manager"].lower()
        )

        dashboard = load_dashboard(
            session["manager"].lower()
        )

        report = None

        if dashboard["completed_rounds"] > 0:
            report = load_report(
                dashboard["completed_rounds"]
            )

        ranking = calculate_table()

        return render_template(
            "dashboard.html",
            manager=manager,
            dashboard=dashboard,
            ranking=ranking,
            report=report,
            active_page="home"
        )

    managers = load_managers()

    summary = get_league_summary()

    return render_template(
        "index.html",
        managers=managers,
        summary=summary,
        season=get_season(),
        active_page="home"
    )

# =========================
# LOGIN
# =========================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if "username" in session:

        return redirect(
            url_for("index")
        )

    if request.method == "POST":

        username = request.form["username"]

        password = request.form.get("password", "")

        user = authenticate(
            username,
            password
        )

        if user:

            session.permanent = True

            session["username"] = user["username"]

            session["role"] = user["role"]

            if "manager" in user:

                session["manager"] = user["manager"]

            return redirect(
                url_for("index")
            )

        return render_template(
            "login.html",
            error="Neplatné uživatelské jméno nebo heslo."
        )

    return render_template(
        "login.html"
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================
# MANAGER
# =========================

@app.route("/manager/<slug>")
def manager(slug):

    manager = load_manager_web(
        slug
    )

    if manager is None:

        return "Manažer nenalezen.", 404

    goalkeepers = [
        p for p in manager["squad"]
        if p["role"] == "P"
    ]

    defenders = [
        p for p in manager["squad"]
        if p["role"] == "D"
    ]

    midfielders = [
        p for p in manager["squad"]
        if p["role"] == "C"
    ]

    forwards = [
        p for p in manager["squad"]
        if p["role"] == "A"
    ]

    return render_template(
        "manager.html",
        manager=manager,
        goalkeepers=goalkeepers,
        defenders=defenders,
        midfielders=midfielders,
        forwards=forwards,
        active_page="league"
    )


# =========================
# LEAGUE
# =========================

@app.route("/league")
def league():

    if "username" not in session:

        return redirect(
            url_for("login")
        )

    season = get_season()

    table = load_table()

    rounds = load_fixture()

    return render_template(
        "league.html",
        table=table,
        rounds=rounds,
        season=season,
        active_page="league"
    )


# =========================
# TEAM
# =========================

@app.route("/team")
def team():

    if "username" not in session:

        return redirect(
            url_for("login")
        )

    if session["role"] != "manager":

        return redirect(
            url_for("index")
        )

    manager = load_manager_web(
        session["manager"].lower()
    )

    goalkeepers = [
        p for p in manager["squad"]
        if p["role"] == "P"
    ]

    defenders = [
        p for p in manager["squad"]
        if p["role"] == "D"
    ]

    midfielders = [
        p for p in manager["squad"]
        if p["role"] == "C"
    ]

    forwards = [
        p for p in manager["squad"]
        if p["role"] == "A"
    ]

    return render_template(
        "team.html",
        manager=manager,
        goalkeepers=goalkeepers,
        defenders=defenders,
        midfielders=midfielders,
        forwards=forwards,
        active_page="team"
    )


# =========================
# LINEUP
# =========================

@app.route(
    "/lineup",
    methods=["GET", "POST"]
)
def lineup():

    if "username" not in session:

        return redirect(
            url_for("login")
        )

    if session["role"] != "manager":

        return redirect(
            url_for("index")
        )

    manager_name = session["manager"].lower()

    # =========================
    # SAVE
    # =========================

    if request.method == "POST":

        if is_lineup_locked():

            flash(
                "🔒 Sestava je uzamčena.",
                "danger"
            )

            return redirect(
                url_for("lineup")
            )

        data = request.get_json()

        success, message = save_current_lineup(
            manager_name,
            data["formation"],
            data["starting"],
            data["bench"]
        )

        return {
            "success": success,
            "message": message
        }


    # =========================
    # LOAD
    # =========================

    manager = load_manager_web(
        manager_name
    )

    lineup = get_current_lineup(
        manager_name
    )

    lineup = expand_lineup(
        manager_name,
        lineup
    )

    lineup = group_lineup(
        lineup
    )

    formation_map = {
        "3-4-3": {
            "defenders": 3,
            "midfielders": 4,
            "forwards": 3
        },
        "3-5-2": {
            "defenders": 3,
            "midfielders": 5,
            "forwards": 2
        },
        "4-3-3": {
            "defenders": 4,
            "midfielders": 3,
            "forwards": 3
        },
        "4-4-2": {
            "defenders": 4,
            "midfielders": 4,
            "forwards": 2
        },
        "4-5-1": {
            "defenders": 4,
            "midfielders": 5,
            "forwards": 1
        },
        "5-3-2": {
            "defenders": 5,
            "midfielders": 3,
            "forwards": 2
        },
        "5-4-1": {
            "defenders": 5,
            "midfielders": 4,
            "forwards": 1
        }
    }

    formation = formation_map[lineup["formation"]]

    return render_template(
        "lineup_v2.html",
        lineup=lineup,
        squad=manager["squad"],
        formation=formation,
        locked=is_lineup_locked(),
        active_page="lineup"
    )


# =========================
# TRANSFERS
# =========================

@app.route("/transfers", methods=["GET", "POST"])
def transfers():
    return transfers_route()

# =========================
# LOAD ROUND
# =========================

@app.route("/round/<int:round_number>")
def round_page(round_number):

    data = load_round(round_number)

    return render_template(
        "round.html",
        data=data,
        round_number=round_number
    )


# =========================
# ROUND NUMBER
# =========================

@app.route("/match/<int:round_number>/<home_slug>-<away_slug>")
def match_page(round_number, home_slug, away_slug):

    data = load_round(round_number)

    match = None

    for m in data["matches"]:

        if (
            m["home_slug"] == home_slug
            and
            m["away_slug"] == away_slug
        ):

            match = m
            break

    if match is None:
        return "Zápas nenalezen", 404

    return render_template(
        "match.html",
        round_number=round_number,
        match=match
    )


# =========================
# PROFILE
# =========================

@app.route("/profile")
def profile():

    if "username" not in session:

        return redirect(
            url_for("login")
        )

    manager = None

    if session["role"] == "manager":

        manager = load_manager_web(
            session["manager"].lower()
        )

    return render_template(
        "profile.html",
        manager=manager,
        season=get_season(),
        active_page="profile"
    )


# =========================
# MATCH PREVIEW
# =========================

@app.route("/match-preview/<int:round_number>/<int:match_index>")
def match_preview(round_number, match_index):

    if "username" not in session:

        return redirect(
            url_for("login")
        )

    matches = load_round_fixtures(
        round_number
    )

    if match_index >= len(matches):

        return "Zápas nebyl nalezen."

    home = matches[match_index][0]
    away = matches[match_index][1]

    home_lineup = group_lineup(
        expand_lineup(
            get_current_lineup(
                home.lower()
            )
        )
    )

    away_lineup = group_lineup(
        expand_lineup(
            get_current_lineup(
                away.lower()
            )
        )
    )

    return str(home_lineup)


# =========================
# PLAYER
# =========================

app.add_url_rule(
    "/player/<int:player_id>",
    endpoint="player",
    view_func=player_route
)


# =========================
# START
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )