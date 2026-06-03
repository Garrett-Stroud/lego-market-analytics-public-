from dataclasses import dataclass
from datetime import datetime

@dataclass
class FeatureVector:
    features: dict


class FeatureBuilder:
    CURRENT_YEAR = datetime.now().year

    def build(self, attrs, enriched) -> FeatureVector:
        """
        attrs: LegoAttributes (from extraction)
        enriched: RebrickableData (from enrichment)
        """

        # --- Basic numeric features ---
        year = enriched.year or 0
        age_years = max(0, self.CURRENT_YEAR - year) if year else 0

        num_parts = enriched.num_parts or 0
        num_minifigs = enriched.num_minifigs or 0

        price = attrs.price or 0.0
        shipping = attrs.shipping_price or 0.0
        total_price = price + shipping

        price_per_part = (price / num_parts) if num_parts > 0 else 0.0

        # --- Theme features ---
        theme = (enriched.theme or "").lower()
        subtheme = (enriched.subtheme or "").lower()

        is_star_wars = 1 if "star wars" in theme else 0
        is_creator = 1 if "creator" in theme else 0
        is_ideas = 1 if "ideas" in theme else 0
        is_botanical = 1 if "botanical" in theme else 0
        is_seasonal = 1 if "seasonal" in theme or "holiday" in theme else 0

        # --- Set type heuristics ---
        is_polybag = 1 if num_parts < 60 else 0
        is_gwp = 1 if "gift" in attrs.title.lower() or "gwp" in attrs.title.lower() else 0

        # --- Build final vector ---
        fv = {
            "age_years": age_years,
            "num_parts": num_parts,
            "num_minifigs": num_minifigs,
            "price": price,
            "shipping": shipping,
            "total_price": total_price,
            "price_per_part": price_per_part,

            # theme indicators
            "is_star_wars": is_star_wars,
            "is_creator": is_creator,
            "is_ideas": is_ideas,
            "is_botanical": is_botanical,
            "is_seasonal": is_seasonal,

            # set type
            "is_polybag": is_polybag,
            "is_gwp": is_gwp,
        }

        return FeatureVector(fv)
