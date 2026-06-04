from fastapi import APIRouter
from dashboard.api.dto.snapshot_dto import SnapshotDTO
from pipeline.storage.snapshot_repository import SnapshotRepository

router = APIRouter(prefix="/snapshots", tags=["snapshots"])

repo = SnapshotRepository()

@router.get("/{set_number}", response_model=list[SnapshotDTO])
def get_snapshots_for_set(set_number: str):
    return repo.get_by_set_number(set_number)
