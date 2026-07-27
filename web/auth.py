import json

from pathlib import Path


# =========================
# PATHS
# =========================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"

USERS_FILE = DATA_DIR / "users.json"


# =========================
# LOAD USERS
# =========================

def load_users():

    with open(
        USERS_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# FIND USER
# =========================

def find_user(username):

    users = load_users()

    for user in users:

        if (
            user["username"].lower()
            ==
            username.lower()
        ):

            return user

    return None


# =========================
# AUTHENTICATE
# =========================

def authenticate(
    username,
    password
):

    user = find_user(
        username
    )

    if user is None:

        return None

    # Administrátor musí zadat heslo
    if user["role"] == "admin":

        if user["password"] != password:

            return None

    # Manažeři heslo nepotřebují

    return user