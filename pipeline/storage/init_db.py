from pathlib import Path
import json

from pipeline.paths import STORAGE_DIR, DATA_DIR
from pipeline.storage.db import get_connection
from pipeline.storage.opportunity_repository import OpportunityRepository

SCHEMA_PATH = STORAGE_DIR / "schema.sql"

def load_json(path: str):
    return json.loads(Path(path).read_text())

def init_db():
    # Ensure schema is applied
    conn = get_connection()
    cur = conn.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cur.executescript(f.read())

    conn.commit()
    conn.close()

    # Insert demo data
    repo = OpportunityRepository()
    run_id = repo.create_run()

    demo_files = [
        DATA_DIR / "examples" / "06_opportunity.json",
        DATA_DIR / "examples" / "07_opportunity.json",
        DATA_DIR / "examples" / "08_opportunity.json",
    ]

    for file in demo_files:
        opp = load_json(file)
        repo.save(run_id, opp)

if __name__ == "__main__":
    init_db()
    print("Database initialized with demo opportunities.")
