from pipeline.canonicalization.sold_batch_validator import validate_sold_batch


def test_batch_validator_mixed():
    raw_listings = [
        {
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
        },
        {
            "item_id": "2",
            "title": None,  # invalid
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
    ]

    canonical, errors = validate_sold_batch(raw_listings, "1234")


    assert len(canonical) == 1
    assert len(errors) == 1
    assert canonical[0].item_id == "1"
