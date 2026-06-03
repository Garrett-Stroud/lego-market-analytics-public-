# canonical/adapters/browse_adapter.py

from models.active_item import CanonicalItem
from pipeline.canonicalization.prices import extract_shipping_price
from pipeline.canonicalization.set_number_extractor import SetNumberExtractor


def from_browse(raw: dict, set_extractor: SetNumberExtractor) -> CanonicalItem:
    title = raw.get("title", "")
    set_number = set_extractor.extract(title)

    sku = raw.get("itemId")

    url = raw.get("itemWebUrl") or raw.get("itemHref")

    price_obj = raw.get("price", {})
    price = float(price_obj.get("value", 0.0))
    currency = price_obj.get("currency", "USD")

    condition = raw.get("condition", "")

    seller = raw.get("seller", {})
    seller_username = seller.get("username", "")

    shipping_price = extract_shipping_price(raw)

    leaf_ids = raw.get("leafCategoryIds", [])
    category_id = leaf_ids[0] if leaf_ids else ""

    total_price = price + shipping_price

    return CanonicalItem(
        sku=sku,
        source="ebay_browse",
        url=url,
        price=price,
        currency=currency,
        condition=condition,
        seller_username=seller_username,
        shipping_price=shipping_price,
        category_id=category_id,
        total_price=total_price,
        raw=raw,
        set_number=set_number,
        title=title,
    )
