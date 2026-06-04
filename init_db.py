from pipeline.storage.init_db import init_db
from pipeline.storage.opportunity_repository import OpportunityRepository
from pathlib import Path
import json

if __name__ == "__main__":
    print("Initializing database...")
    init_db()

    repo = OpportunityRepository()

    # Load demo opportunity
    demo_path = Path("data/examples/06_opportunity.json")
    demo = json.loads(demo_path.read_text())

    run_id = repo.create_run()
    repo.save(str(run_id), demo)


    print("Database initialized with demo opportunity.")
