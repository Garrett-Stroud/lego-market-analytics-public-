from pydantic import BaseModel
from typing import Optional

class SnapshotDTO(BaseModel):
    set_number: str
    rb_name: Optional[str]
    rb_theme: Optional[str]
    rb_year: Optional[int]

    active_lowest: Optional[float]
    active_median: Optional[float]
    active_count: int

    sold_median: Optional[float]
    sold_count: int
    trend: Optional[float]
    volatility: Optional[float]
