from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CORE_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
PIPELINE_DIR = PROJECT_ROOT / "pipeline"
CONFIG_DIR = PIPELINE_DIR / "config"
STORAGE_DIR = PIPELINE_DIR / "storage"
