import json
from pathlib import Path

from transfers.ownership import get_owned_coaches


PROJECT_DIR = Path(__file__).resolve().parent.parent

COACHES_FILE = PROJECT_DIR / "data" / "coaches.json"


def load_coaches():

    with open(
        COACHES_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)