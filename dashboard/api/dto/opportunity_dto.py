from pydantic import BaseModel
from typing import Optional, Dict, Any

class OpportunityDTO(BaseModel):
    id: Optional[int] = None
    product_key: str

    title: Optional[str] = None
    image_url: Optional[str] = None   # <-- REQUIRED

    buy_price: float
    sell_price: float
    profit: float
    roi: float
    score: float

    buy_url: Optional[str] = None
    sell_url: Optional[str] = None

    score_details: Dict[str, Any] = {}
