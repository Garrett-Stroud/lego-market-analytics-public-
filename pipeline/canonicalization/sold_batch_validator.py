# canonical/validators/sold_batch_validator.py
from pipeline.canonicalization.sold_adapter import from_sold
from pipeline.canonicalization.sold_validator import validate_sold_item


def validate_sold_batch(raw_listings, set_number):
    """
    Validate a batch of raw extraction listings.
    Returns:
        canonical_items: list of CanonicalSoldItem
        errors: list of (item_id, error_message)
    """
    canonical_items = []
    errors = []

    for raw in raw_listings:
        item_id = raw.get("item_id")

        try:
            canonical = from_sold(raw, set_number)
            validate_sold_item(canonical)
            canonical_items.append(canonical)


        except Exception as e:
            print("VALIDATION ERROR:", item_id, e)
            errors.append((item_id, str(e)))

    return canonical_items, errors
