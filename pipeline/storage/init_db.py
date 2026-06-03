from pathlib import Path
from core.paths import STORAGE_DIR
from pipeline.storage.db import get_connection

SCHEMA_PATH = Path(STORAGE_DIR / "schema.sql")

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        cur.executescript(f.read())

    conn.commit()
    conn.close()
