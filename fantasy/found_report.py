import json
from pathlib import Path

def generate_round_report(round_number):
    report = {
        "version": 1,
        "round": round_number,
        "generated": None,
        "matches": [],
        "lineups": {},
        "table": [],
        "awards": {}
    }

    output = Path("data/rounds")
    output.mkdir(parents=True, exist_ok=True)

    with open(
        output / f"round_{round_number:02}.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(report, f, ensure_ascii=False, indent=4)