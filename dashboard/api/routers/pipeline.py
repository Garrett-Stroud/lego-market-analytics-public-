from fastapi import APIRouter
import subprocess
import sys
from pathlib import Path

router = APIRouter(prefix="/pipeline", tags=["pipeline"])

@router.post("/run")
def run_pipeline():
    # Path to your pipeline script
    pipeline_path = Path(__file__).resolve().parents[3] / "pipeline" / "run_scoring_pipeline.py"

    # Launch pipeline in a separate process
    subprocess.Popen([sys.executable, str(pipeline_path)])

    return {"status": "started"}
