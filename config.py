"""Application configuration."""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration shared by all environments."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "library.db")
    )
    SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


class TestConfig(Config):
    """Configuration used by the automated test suite.

    DATABASE_PATH is overridden per test-run with a temporary file path
    (see tests/test_app.py) since Flask opens a fresh sqlite3 connection
    per request/app-context, and a bare ":memory:" DB would not persist
    data between those connections.
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
