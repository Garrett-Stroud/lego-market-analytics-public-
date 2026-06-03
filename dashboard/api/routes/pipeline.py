from fastapi import APIRouter
import asyncio
import threading

from pipeline.run_scoring_pipeline import run_scoring_pipeline

router = APIRouter()

def run_async_pipeline():
    asyncio.run(run_scoring_pipeline())

@router.post("/pipeline/run")
def trigger_pipeline():
    # Run in background thread so API returns immediately
    thread = threading.Thread(target=run_async_pipeline)
    thread.start()
    return {"status": "started"}
