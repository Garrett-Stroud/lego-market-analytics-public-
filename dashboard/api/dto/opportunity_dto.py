from pydantic import BaseModel
from typing import Optional, Dict

class OpportunityDTO(BaseModel):
    product_key: str
    buy_price: float
    sell_price: float
    profit: float
    roi: float
    score: float
    buy_url: Optional[str]
    score_details: Dict
