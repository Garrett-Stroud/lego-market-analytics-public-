# canonical/active_item.py

from dataclasses import dataclass

from pipeline.canonicalization import browse_adapter


@dataclass
class CanonicalItem:
    sku: str
    source: str
    url: str
    price: float
    currency: str
    condition: str
    seller_username: str
    shipping_price: float
    category_id: str
    total_price: float
    raw: dict
    title: str | None = None
    set_number: str | None = None


def to_canonical_item(raw: dict, source: str) -> CanonicalItem:
    if source == "ebay_browse":
        return browse_adapter.from_browse(raw)

    raise ValueError(f"Unknown canonicalization source: {source}")
