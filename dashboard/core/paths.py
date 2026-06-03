from pathlib import Path

# This file's directory: core/
CORE_DIR = Path(__file__).resolve().parent

# Project root: one level up from core/
PROJECT_ROOT = CORE_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
PIPELINE_DIR = PROJECT_ROOT / "pipeline"
CONFIG_DIR = PIPELINE_DIR / "config"
STORAGE_DIR = PIPELINE_DIR / "storage"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"
