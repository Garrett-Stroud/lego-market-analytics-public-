from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
PIPELINE_DIR = PROJECT_ROOT / "pipeline"
CONFIG_DIR = PIPELINE_DIR / "config"
STORAGE_DIR = PIPELINE_DIR / "storage"

DB_PATH = DATA_DIR / "opportunities.db"
SCHEMA_PATH = STORAGE_DIR / "schema.sql"
