from bs4 import BeautifulSoup


def parse():

    with open("page_playwright.html", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    players = []
    coaches = {}

    teams = soup.select("li.team-table")

    for team in teams:

        team_name = team.select_one(".team-name").get_text(strip=True)

        rows = team.select("tbody tr")

        for row in rows:

            name = row.select_one(".player-name")

            if not name:
                continue

            grades = row.select(".player-grade")

            if len(grades) < 3:
                continue

            grade_tag = grades[2]

            grade = grade_tag.get("data-value")

            if not grade:
                continue

            # SV (Senza Voto) - hráč se nepočítá
            if grade == "55":
                continue

            role_tag = row.select_one(".role")

            role = role_tag["data-value"].upper()

            if role == "ALL":
                coaches[name.get_text(strip=True)] = grade
                continue

            link = row.select_one(".player-link")

            player_id = None

            if link:
                href = link["href"]
                player_id = href.split("/")[-2]

            player = {
                "id": player_id,
                "team": team_name,
                "role": role,
                "name": name.get_text(strip=True),
                "grade": grade
            }

            players.append(player)

    
    return players, coaches