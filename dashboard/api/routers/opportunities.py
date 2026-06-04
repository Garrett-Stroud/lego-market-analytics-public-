from fastapi import APIRouter
from dashboard.api.dto.opportunity_dto import OpportunityDTO
from pipeline.storage.opportunity_repository import OpportunityRepository

router = APIRouter(prefix="/opportunities", tags=["opportunities"])

repo = OpportunityRepository()

@router.get("/latest", response_model=list[OpportunityDTO])
def get_latest_opportunities():
    run_id = repo.get_latest_run_id()
    return repo.get_by_run(run_id)

@router.get("/{set_number}", response_model=list[OpportunityDTO])
def get_opportunities_for_set(set_number: str):
    return repo.get_by_set_number(set_number)
