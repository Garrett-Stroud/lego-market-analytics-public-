# canonical/helpers/condition.py

def normalize_condition(raw_condition: str):
    """
    Normalize condition strings into a consistent format.
    """
    if not raw_condition:
        return None

    c = raw_condition.lower().strip()

    # common eBay condition variants
    if "new" in c:
        return "new"
    if "used" in c:
        return "used"
    if "open box" in c:
        return "open_box"
    if "damaged" in c:
        return "damaged"
    if "refurb" in c:
        return "refurbished"

    return c
