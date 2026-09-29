"""Database connection handling for the Library Management System.

Uses sqlite3 directly (no ORM) so the SQL and schema design are explicit
and easy to reason about / diagram.
"""
import sqlite3

from flask import current_app, g


def get_db():
    """Return a request-scoped SQLite connection, creating it if needed."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    """Close the database connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Create tables (if they don't exist yet) and register teardown."""
    with app.app_context():
        db = get_db()
        with open(app.config["SCHEMA_PATH"], "r", encoding="utf-8") as f:
            db.executescript(f.read())
        db.commit()
    app.teardown_appcontext(close_db)
