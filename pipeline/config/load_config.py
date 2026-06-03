import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "pipeline_config.json"

def load_pipeline_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)
