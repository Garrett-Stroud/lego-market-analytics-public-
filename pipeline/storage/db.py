from pipeline.paths import DB_PATH
import sqlite3

def get_connection():
    # Ensure parent directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
