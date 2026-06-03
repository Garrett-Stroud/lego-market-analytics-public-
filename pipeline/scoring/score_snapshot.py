from models.active_item import CanonicalItem
from models.joined_set_snapshot import JoinedSetSnapshot
from models.opportunity import Opportunity


def score_snapshot(
    snapshot: JoinedSetSnapshot,
    active_items: list[CanonicalItem],
) -> Opportunity | None:

    if not snapshot.sold_median or not active_items:
        return None

    # pick lowest active listing
    active_items_sorted = sorted(active_items, key=lambda x: x.total_price)
    buy = active_items_sorted[0]

    buy_price = buy.total_price
    sell_price = snapshot.sold_median

    if buy_price <= 0:
        return None

    profit = sell_price - buy_price
    roi = profit / buy_price
    score = roi  # baseline score

    return Opportunity(
        product_key=snapshot.set_number,

        buy_source="ebay",
        buy_price=buy_price,
        buy_url=buy.url,

        sell_source="ebay",
        sell_price=sell_price,
        sell_url=None,  # no sell URL for sold median

        profit=profit,
        roi=roi,
        score=score,
        score_details={
            "active_lowest": buy_price,
            "sold_median": sell_price,
            "active_count": snapshot.active_count,
            "sold_count": snapshot.sold_count,
        }
    )
