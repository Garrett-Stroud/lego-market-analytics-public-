import re
from dataclasses import dataclass

from models.active_item import CanonicalItem


@dataclass
class LegoAttributes:
    set_number: str | None
    theme: str | None
    subtheme: str | None
    piece_count: int | None
    minifig_count: int | None
    is_polybag: bool
    is_bulk_lot: bool
    is_retired: bool | None
    title: str
    price: float | None
    shipping_price: float | None
    total_price: float | None


THEMES = {
    "star wars": "Star Wars",
    "harry potter": "Harry Potter",
    "technic": "Technic",
    "city": "City",
    "friends": "Friends",
    "ninjago": "Ninjago",
    "marvel": "Marvel",
    "dc": "DC",
    "creator": "Creator",
    "minecraft": "Minecraft",
    "disney": "Disney",
}


class AttributeExtractor:

    SET_REGEX = re.compile(r"\b(\d{3,5})\b")
    PIECES_REGEX = re.compile(r"(\d+)\s*(pcs|pieces)")
    MINIFIG_REGEX = re.compile(r"(\d+)\s*(minifig|minifigs|minifigure|minifigures)")

    def extract(self, item: CanonicalItem) -> LegoAttributes:
        title = item.raw.get("title", "")
        norm = title.lower()

        # --- set number ---
        set_number = None
        m = self.SET_REGEX.search(norm)
        if m:
            set_number = m.group(1)

            # 🔥 Normalize to Rebrickable format (40300 → 40300-1)
            if "-" not in set_number:
                set_number = f"{set_number}-1"

        # --- theme ---
        theme = None
        for key, val in THEMES.items():
            if key in norm:
                theme = val
                break

        # --- polybag ---
        is_polybag = (
            "polybag" in norm
            or (set_number and set_number.startswith(("30", "40", "50")))
        )

        # --- bulk lot ---
        is_bulk_lot = any(word in norm for word in ["lot", "bulk", "pound", "lbs"])

        # --- piece count ---
        piece_count = None
        m = self.PIECES_REGEX.search(norm)
        if m:
            piece_count = int(m.group(1))

        # --- minifig count ---
        minifig_count = None
        m = self.MINIFIG_REGEX.search(norm)
        if m:
            minifig_count = int(m.group(1))

        return LegoAttributes(
            set_number=set_number,
            theme=theme,
            subtheme=None,
            piece_count=piece_count,
            minifig_count=minifig_count,
            is_polybag=is_polybag,
            is_bulk_lot=is_bulk_lot,
            is_retired=None,
            title=title,
            price=item.price,
            shipping_price=item.shipping_price,
            total_price=item.total_price
        )
