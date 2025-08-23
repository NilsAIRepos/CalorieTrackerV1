"""SQLite persistence helpers."""

import sqlite3
from pathlib import Path

DB_PATH = Path("user_data.db")


def get_conn() -> sqlite3.Connection:
    """Return a connection to the user-side database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the entries table if it does not exist."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            calories INTEGER NOT NULL,
            details TEXT
        )
        """
    )
    conn.commit()
    conn.close()


# Initialize database on import
init_db()
