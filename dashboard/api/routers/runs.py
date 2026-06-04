from fastapi import APIRouter
from dashboard.api.dto.run_dto import RunDTO
from pipeline.storage.opportunity_repository import OpportunityRepository
from pipeline.storage.snapshot_repository import SnapshotRepository

router = APIRouter(prefix="/runs", tags=["runs"])

snap_repo = SnapshotRepository()
opp_repo = OpportunityRepository()

@router.get("/", response_model=list[RunDTO])
def list_runs():
    return snap_repo.get_all_runs()

@router.get("/{run_id}/opportunities")
def get_run_opportunities(run_id: str):
    return opp_repo.get_by_run(run_id)

@router.get("/{run_id}/snapshots")
def get_run_snapshots(run_id: str):
    return snap_repo.get_by_run(run_id)
