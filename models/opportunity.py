from pydantic import BaseModel
from typing import Optional, Dict

class Opportunity(BaseModel):
    product_key: str


    product_title: Optional[str] = None
    image_url: Optional[str] = None

    buy_source: str
    buy_price: float
    buy_url: Optional[str]

    sell_source: str
    sell_price: float
    sell_url: Optional[str]

    profit: float
    roi: float
    score: float
    score_details: Dict
