from pipeline.canonicalization.sold_adapter import from_sold
from pipeline.canonicalization.set_number_extractor import SetNumberExtractor


def validate_sold_adapter(raw_listings):
    errors = []
    canonical_items = []

    set_extractor = SetNumberExtractor()

    for raw in raw_listings:
        try:
            item = from_sold(raw, set_extractor)
            canonical_items.append(item)
        except Exception as e:
            errors.append((raw.get("itemId"), str(e)))

    return canonical_items, errors
