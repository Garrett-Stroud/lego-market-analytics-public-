from statistics import median
from models.joined_set_snapshot import JoinedSetSnapshot

class ActiveSoldJoiner:
    def __init__(self, rb_index: dict):
        self.rb_index = rb_index

    def join(self, active_groups: dict, sold_features: dict) -> dict:
        """
        Returns dict[set_number -> JoinedSetSnapshot]
        """
        snapshots = {}

        for set_num, active_items in active_groups.items():
            rb = self.rb_index.get(set_num, {})

            # Active stats
            active_prices = sorted(i.total_price for i in active_items)
            active_lowest = active_prices[0] if active_prices else None
            active_median = median(active_prices) if active_prices else None
            active_count = len(active_items)

            # Sold stats
            sold = sold_features.get(set_num, {})
            sold_median = sold.get("median_sold_price")
            sold_min = sold.get("min_sold_price")
            sold_max = sold.get("max_sold_price")
            sold_count = sold.get("sold_count", 0)

            snapshots[set_num] = JoinedSetSnapshot(
                set_number=set_num,

                rb_name=rb.get("name"),
                rb_theme=rb.get("theme"),
                rb_year=rb.get("year"),
                rb_num_parts=rb.get("num_parts"),

                active_lowest=active_lowest,
                active_median=active_median,
                active_count=active_count,

                sold_median=sold_median,
                sold_min=sold_min,
                sold_max=sold_max,
                sold_count=sold_count,

                sold_count_30d=sold.get("sold_count_30d"),
                sold_count_90d=sold.get("sold_count_90d"),
                volatility=sold.get("volatility"),
                trend=sold.get("trend"),
            )

        return snapshots
