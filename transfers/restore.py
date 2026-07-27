import shutil

from pathlib import Path


# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"

BACKUP_DIR = PROJECT_DIR / "backups"


# =========================
# LIST BACKUPS
# =========================

def list_backups(manager_name):

    files = []

    manager_backup_dir = (
        BACKUP_DIR /
        manager_name
    )

    if not manager_backup_dir.exists():

        return []

    for file in manager_backup_dir.glob(
        "*.json"
    ):

        files.append(file)

    files.sort(
        reverse=True
    )

    return files


# =========================
# RESTORE BACKUP
# =========================

def restore_backup(
    manager_name,
    backup_file
):

    destination = (
        DATA_DIR /
        manager_name /
        "squad.json"
    )

    shutil.copy2(
        backup_file,
        destination
    )