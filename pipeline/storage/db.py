from pathlib import Path
import sqlite3
from core.paths import DATA_DIR


def get_connection():
    db_path = DATA_DIR / "arbitrage.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn