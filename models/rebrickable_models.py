from dataclasses import dataclass

@dataclass
class RebrickableData:
    name: str | None
    year: int | None
    theme: str | None
    subtheme: str | None
    num_parts: int | None
    num_minifigs: int | None
    image_url: str | None
    median_price: float | None
    raw: dict | None

def to_dict(self):
    return {
        "name": self.name,
        "year": self.year,
        "theme": self.theme,
        "subtheme": self.subtheme,
        "num_parts": self.num_parts,
        "num_minifigs": self.num_minifigs,
        "image_url": self.image_url,
        "median_price": self.median_price,
        "theme_family": self.theme_family,
        "theme_path": self.theme_path,
        "theme_depth": self.theme_depth,
        "retired_year": self.retired_year,
    }
