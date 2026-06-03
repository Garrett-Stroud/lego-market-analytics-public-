from models.sold_item import CanonicalSoldItem


def canonicalize_raw_sold_snapshot(raw: dict) -> CanonicalSoldItem:
    raw_set_number = raw["set_number"]

    # Normalize here
    if "-" not in raw_set_number:
        canonical_set_number = f"{raw_set_number}-1"
    else:
        canonical_set_number = raw_set_number

    return CanonicalSoldItem(
        set_number=canonical_set_number,
        item_id=raw["item_id"],
        title=raw["title"],
        condition=raw["condition"],
        completeness=raw.get("completeness"),
        has_minifigs=raw.get("has_minifigs", False),
        has_box=raw.get("has_box", False),
        has_instructions=raw.get("has_instructions", False),
        sold_price=raw["sold_price"],
        shipping_price=raw["shipping_price"],
        total_price=raw["total_price"],
        sold_timestamp=raw["sold_timestamp"],
        sold_date=raw["sold_date"],
        seller_username=raw.get("seller_username"),
        seller_feedback_pct=raw.get("seller_feedback_pct"),
        seller_feedback_count=raw.get("seller_feedback_count"),
        is_auction=raw["is_auction"],
        is_buy_it_now=raw["is_buy_it_now"],
        is_best_offer=raw["is_best_offer"],
        raw_html=raw["raw_html"],
    )
