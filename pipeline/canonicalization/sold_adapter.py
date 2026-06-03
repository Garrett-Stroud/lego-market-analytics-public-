from models.sold_item import CanonicalSoldItem
from pipeline.canonicalization.set_number_extractor import SetNumberExtractor
from pipeline.canonicalization.sold_validator import validate_sold_item
from pipeline.canonicalization.date_utils import iso_to_timestamp
from pipeline.canonicalization.prices import normalize_price, compute_total_price


def from_sold(raw: dict, set_extractor: SetNumberExtractor) -> CanonicalSoldItem:
    """
    Public adapter entry point.
    Converts a raw sold listing into a validated CanonicalSoldItem.
    """
    item = from_sold_raw(raw, set_extractor)
    validate_sold_item(item)
    return item


def from_sold_raw(raw: dict, set_extractor: SetNumberExtractor) -> CanonicalSoldItem:
    title = raw.get("title", "")
    url = raw.get("itemWebUrl") or raw.get("itemHref")

    # --- price ---
    price_obj = raw.get("price", {})
    price = normalize_price(price_obj)

    shipping_price = 0.0
    shipping_options = raw.get("shippingOptions", [])
    if shipping_options:
        shipping_price = normalize_price(shipping_options[0].get("shippingCost", {}))

    total_price = compute_total_price(price, shipping_price)
    currency = price_obj.get("currency", "USD")

    # --- sold date ---
    date_sold = raw.get("itemEndDate") or raw.get("itemCreationDate")
    sold_timestamp = iso_to_timestamp(date_sold)
    sold_date = date_sold.split("T")[0] if date_sold else None

    # --- seller ---
    seller = raw.get("seller", {})
    seller_username = seller.get("username")
    seller_feedback_pct = float(seller.get("feedbackPercentage", 0) or 0)
    seller_feedback_count = int(seller.get("feedbackScore", 0) or 0)

    # --- condition ---
    condition = raw.get("condition")

    # --- buying options ---
    buying_opts = raw.get("buyingOptions", [])
    is_auction = "AUCTION" in buying_opts
    is_buy_it_now = "FIXED_PRICE" in buying_opts
    is_best_offer = "BEST_OFFER" in buying_opts

    # --- completeness heuristics ---
    lower = title.lower()
    completeness = None
    if "complete" in lower:
        completeness = "complete"
    elif "incomplete" in lower:
        completeness = "incomplete"

    has_minifigs = any(word in lower for word in ["minifig", "minifigure", "fig"])
    has_box = "box" in lower
    has_instructions = "instruction" in lower or "manual" in lower

    # --- set number ---
    set_number = set_extractor.extract(title)

    return CanonicalSoldItem(
        item_id=raw.get("itemId"),
        title=title,
        url=url,

        price=price,
        shipping_price=shipping_price,
        total_price=total_price,
        currency=currency,

        date_sold=date_sold,
        sold_timestamp=sold_timestamp,
        sold_date=sold_date,

        condition=condition,
        seller_username=seller_username,
        seller_feedback_pct=seller_feedback_pct,
        seller_feedback_count=seller_feedback_count,

        completeness=completeness,
        has_minifigs=has_minifigs,
        has_box=has_box,
        has_instructions=has_instructions,

        is_auction=is_auction,
        is_buy_it_now=is_buy_it_now,
        is_best_offer=is_best_offer,

        set_number=set_number,
        raw_html=None,
        raw=raw,
    )
