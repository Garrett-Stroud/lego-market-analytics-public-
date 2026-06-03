from pydantic import BaseModel
from typing import Optional

class JoinedSetSnapshot(BaseModel):
    set_number: str

    # Rebrickable metadata
    rb_name: Optional[str]
    rb_theme: Optional[str]
    rb_year: Optional[int]
    rb_num_parts: Optional[int]

    # Active listing stats
    active_lowest: Optional[float]
    active_median: Optional[float]
    active_count: int

    # Sold listing stats
    sold_median: Optional[float]
    sold_min: Optional[float]
    sold_max: Optional[float]
    sold_count: int

    # Demand / trend
    sold_count_30d: Optional[int] = None
    sold_count_90d: Optional[int] = None
    volatility: Optional[float] = None
    trend: Optional[float] = None
