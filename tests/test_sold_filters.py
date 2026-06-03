class FakeAttrs:
    def __init__(
        self,
        title="",
        is_bulk_lot=False,
        set_number="1234",
        total_price=50,
        sold_timestamp=123456,
        condition="Used",
        listing_type="FIXED_PRICE",
        bid_count=None,
        shipping_price=5,
        seller_feedback_pct=100,
        seller_feedback_count=100,
        piece_count=100,
    ):
        self.title = title
        self.is_bulk_lot = is_bulk_lot
        self.set_number = set_number
        self.total_price = total_price
        self.sold_timestamp = sold_timestamp
        self.condition = condition
        self.listing_type = listing_type
        self.bid_count = bid_count
        self.shipping_price = shipping_price
        self.seller_feedback_pct = seller_feedback_pct
        self.seller_feedback_count = seller_feedback_count
        self.piece_count = piece_count


class FakeEnriched:
    def __init__(self, **kwargs):
        # You can add fields as needed, but usually the filter doesn't use enriched much
        self.__dict__.update(kwargs)

from features.filters.sold_filters import is_valid_for_sold

def test_filter_rejects_bulk_lot():
    attrs = FakeAttrs(title="LEGO Lot of 5", is_bulk_lot=True)
    enriched = FakeEnriched()
    assert not is_valid_for_sold(attrs, enriched)


def test_filter_accepts_clean_listing():
    attrs = FakeAttrs(title="LEGO 75257 Complete", is_bulk_lot=False)
    enriched = FakeEnriched()
    assert is_valid_for_sold(attrs, enriched)


def test_rejects_incomplete_listing():
    attrs = FakeAttrs(title="LEGO 75257 missing pieces")
    enriched = FakeEnriched()
    assert not is_valid_for_sold(attrs, enriched)

def test_rejects_instructions_only():
    attrs = FakeAttrs(title="LEGO 75257 instructions only")
    enriched = FakeEnriched()
    assert not is_valid_for_sold(attrs, enriched)

def test_rejects_low_feedback_seller():
    attrs = FakeAttrs(
        title="LEGO 75257",
        seller_feedback_pct=95,   # below threshold
        seller_feedback_count=10  # below threshold
    )
    enriched = FakeEnriched()
    assert not is_valid_for_sold(attrs, enriched)

def test_rejects_shipping_outlier():
    attrs = FakeAttrs(
        title="LEGO 75257",
        total_price=50,
        shipping_price=40  # > 50% of total price
    )
    enriched = FakeEnriched()
    assert not is_valid_for_sold(attrs, enriched)
