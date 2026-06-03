from collections import defaultdict
from statistics import median

class SoldFeatureBuilder:
    def __init__(self, rb_index: dict):
        self.rb_index = rb_index

    def build_set_features(self, sold_items):
        by_set = defaultdict(list)
        for item in sold_items:
            if item.set_number:
                by_set[item.set_number].append(item)

        features = {}
        for set_num, items in by_set.items():
            prices = sorted(i.total_price for i in items)
            trimmed = prices[1:-1] if len(prices) >= 5 else prices

            rb = self.rb_index.get(set_num, {})

            features[set_num] = {
                "set_number": set_num,
                "sold_count": len(items),
                "median_sold_price": median(trimmed) if trimmed else None,
                "min_sold_price": min(trimmed) if trimmed else None,
                "max_sold_price": max(trimmed) if trimmed else None,
                "rb_name": rb.get("name"),
                "rb_theme": rb.get("theme"),
                "rb_year": rb.get("year"),
                "rb_num_parts": rb.get("num_parts"),
            }

        return features
