# canonical/validators/sold_validator.py

from models.sold_item import CanonicalSoldItem

ALLOWED_COMPLETENESS = {
    None,
    "complete",
    "incomplete",
    "minifigs_only",
}

def validate_sold_item(item: CanonicalSoldItem):
    """
    Validate a CanonicalSoldItem object.
    Raises ValueError with descriptive messages if invalid.
    """

    # Required fields
    if not item.set_number:
        raise ValueError("Missing set_number")

    if not item.item_id:
        raise ValueError("Missing item_id")

    # Type checks
    if not isinstance(item.sold_price, float):
        raise ValueError(f"sold_price must be float, got {type(item.sold_price)}")

    if not isinstance(item.shipping_price, float):
        raise ValueError(f"shipping_price must be float, got {type(item.shipping_price)}")

    if not isinstance(item.total_price, float):
        raise ValueError(f"total_price must be float, got {type(item.total_price)}")

    if not isinstance(item.sold_timestamp, int):
        raise ValueError(f"sold_timestamp must be int, got {type(item.sold_timestamp)}")

    # Completeness validation
    if item.completeness not in ALLOWED_COMPLETENESS:
        raise ValueError(f"Invalid completeness value: {item.completeness}")

    # Listing type flags
    for flag in ["is_auction", "is_buy_it_now", "is_best_offer"]:
        if not isinstance(getattr(item, flag), bool):
            raise ValueError(f"{flag} must be bool")

    # Seller info (optional but type-checked)
    if item.seller_feedback_pct is not None and not isinstance(item.seller_feedback_pct, int):
        raise ValueError("seller_feedback_pct must be int or None")

    if item.seller_feedback_count is not None and not isinstance(item.seller_feedback_count, int):
        raise ValueError("seller_feedback_count must be int or None")

    # Raw HTML
    if not isinstance(item.raw_html, str):
        raise ValueError("raw_html must be a string")

    return True
