import json
from pathlib import Path

import requests

API_KEY = "2604474ebe7c473da61945316ef9c039"

URL = "https://api.football-data.org/v4/competitions/SA/matches"

headers = {
    "X-Auth-Token": API_KEY
}

response = requests.get(
    URL,
    headers=headers
)

response.raise_for_status()

data = response.json()

rounds = {}

for match in data["matches"]:

    matchday = match["matchday"]

    rounds.setdefault(matchday, [])

    rounds[matchday].append({
        "home": match["homeTeam"]["shortName"],
        "away": match["awayTeam"]["shortName"]
    })

fixtures = []

for round_number in sorted(rounds):

    fixtures.append({
        "round": round_number,
        "matches": rounds[round_number]
    })

OUTPUT_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "serie_a"
    / "fixtures.json"
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        fixtures,
        f,
        ensure_ascii=False,
        indent=4
    )

print("Hotovo.")
print(f"Uloženo {len(fixtures)} kol.")