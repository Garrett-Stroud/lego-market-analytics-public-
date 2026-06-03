from services.canonical.helpers.prices import normalize_price, compute_total_price

def test_normalize_price_numeric():
    assert normalize_price(12.5) == 12.5
    assert normalize_price("12.50") == 12.50
    assert normalize_price("$12.50") == 12.50

def test_normalize_price_dict():
    assert normalize_price({"value": "19.99"}) == 19.99

def test_normalize_price_invalid():
    assert normalize_price(None) == 0.0
    assert normalize_price("not a price") == 0.0

def test_compute_total_price():
    assert compute_total_price(10.0, 5.0) == 15.0
