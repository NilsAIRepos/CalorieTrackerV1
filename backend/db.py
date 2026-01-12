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

    # Enable support for column alterations

    # Create entries table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            calories INTEGER NOT NULL,
            details TEXT,
            protein REAL DEFAULT 0,
            carbs REAL DEFAULT 0,
            fat REAL DEFAULT 0,
            sugar REAL DEFAULT 0
        )
        """
    )

    # Create chat_logs table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Attempt to add columns if they don't exist (migration for existing DBs)
    # This is a simple migration strategy for development
    try:
        cur.execute("ALTER TABLE entries ADD COLUMN protein REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass # Column likely exists

    try:
        cur.execute("ALTER TABLE entries ADD COLUMN carbs REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    try:
        cur.execute("ALTER TABLE entries ADD COLUMN fat REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    try:
        cur.execute("ALTER TABLE entries ADD COLUMN sugar REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


# Initialize database on import
init_db()
