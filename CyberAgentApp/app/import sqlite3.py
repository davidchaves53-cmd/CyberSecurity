import sqlite3
from pathlib import Path

DB_PATH = Path("events.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        ip_address TEXT,
        user_agent TEXT,
        timestamp TEXT,
        success INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER,
        risk_level TEXT,
        action TEXT,
        reason TEXT,
        timestamp TEXT,
        FOREIGN KEY(event_id) REFERENCES login_events(id)
    )
    """)

    conn.commit()
    conn.close()
