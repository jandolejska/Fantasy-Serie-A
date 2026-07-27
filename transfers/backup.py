import json
import shutil

from pathlib import Path
from datetime import datetime


# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"

BACKUP_DIR = PROJECT_DIR / "backups"


BACKUP_DIR.mkdir(
    exist_ok=True
)


# =========================
# CREATE BACKUP
# =========================

def create_backup(manager_name):

    source = (
        DATA_DIR /
        manager_name /
        "squad.json"
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    manager_backup_dir = (
        BACKUP_DIR /
        manager_name
    )

    manager_backup_dir.mkdir(
        exist_ok=True
    )

    destination = (
        manager_backup_dir /
        f"{timestamp}.json"
    )

    shutil.copy2(
        source,
        destination
    )