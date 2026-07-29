import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    PERMANENT_SESSION_LIFETIME = timedelta(days=365)

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Na serveru přepneme na True
    SESSION_COOKIE_SECURE = False


