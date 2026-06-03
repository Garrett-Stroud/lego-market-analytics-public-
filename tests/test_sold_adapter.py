from sold.sold_adapters import from_sold


def test_sold_adapter_basic():
    raw = {
        "item_id": "1",
        "title": "LEGO COMPLETE",
        "condition": "Used",
        "sold_date_raw": "Sold May 28, 2024",
        "price_raw": "$10.00",
        "shipping_raw": "$5.00",
        "seller_block_raw": "seller 100% positive (10)",
        "is_auction": False,
        "is_buy_it_now": True,
        "is_best_offer": False,
        "raw_html": "<li></li>"
    }

    item = from_sold(raw, "75192")

    assert item.set_number == "75192"
    assert item.item_id == "1"
    assert item.sold_price == 10.00
    assert item.shipping_price == 5.00
    assert item.total_price == 15.00
    assert item.seller_feedback_pct == 100
    assert item.seller_feedback_count == 10
