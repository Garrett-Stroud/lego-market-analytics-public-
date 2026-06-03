from pydantic import BaseModel
from typing import Optional, Dict

class CanonicalSoldItem(BaseModel):
    item_id: str
    title: str
    url: Optional[str]

    price: float
    shipping_price: float
    total_price: float
    currency: str

    date_sold: Optional[str]
    sold_timestamp: Optional[int]
    sold_date: Optional[str]

    condition: Optional[str]
    seller_username: Optional[str]
    seller_feedback_pct: Optional[float]
    seller_feedback_count: Optional[int]

    completeness: Optional[str]
    has_minifigs: Optional[bool]
    has_box: Optional[bool]
    has_instructions: Optional[bool]

    is_auction: bool
    is_buy_it_now: bool
    is_best_offer: bool

    set_number: Optional[str]
    raw_html: Optional[str] = None

    raw: Dict
