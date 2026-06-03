
# canonical/helpers/prices.py

def normalize_price(value):
    """
    Normalize price-like values into a float.
    Handles:
        - dict with {"value": "..."}
        - string values
        - int/float
        - None
    """
    if value is None:
        return 0.0

    # dict from eBay
    if isinstance(value, dict):
        return float(value.get("value", 0.0))

    # numeric
    if isinstance(value, (int, float)):
        return float(value)

    # string
    if isinstance(value, str):
        try:
            return float(value.replace("$", "").strip())
        except:
            return 0.0

    return 0.0


def compute_total_price(price: float, shipping: float) -> float:
    """
    Compute total price safely.
    """
    try:
        return float(price) + float(shipping)
    except:
        return float(price)

def extract_shipping_price(raw: dict) -> float:
    """
    Extract shipping cost from raw eBay Browse API item.
    Returns 0.0 if missing or malformed.
    """
    try:
        shipping_options = raw.get("shippingOptions", [])
        if not shipping_options:
            return 0.0

        cost_obj = shipping_options[0].get("shippingCost", {})
        return normalize_price(cost_obj)
    except Exception:
        return 0.0
