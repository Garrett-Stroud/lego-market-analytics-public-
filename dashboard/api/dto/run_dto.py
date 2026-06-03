from pydantic import BaseModel

class RunDTO(BaseModel):
    run_id: str
    snapshot_count: int
    opportunity_count: int | None = 0
    created_at: str
