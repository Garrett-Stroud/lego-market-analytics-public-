import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from pipeline.enrichment.rebrickable_index import normalize_set_number


@dataclass
class RebrickableData:
    name: Optional[str]
    year: Optional[int]
    theme: Optional[str]
    theme_family: Optional[str]
    theme_path: List[str]
    theme_depth: Optional[int]
    num_parts: Optional[int]
    num_minifigs: Optional[int]
    image_url: Optional[str]
    retired_year: Optional[int]

    missing_parts: bool
    missing_minifigs: bool
    missing_theme: bool

    raw: Dict[str, Any]


class RebrickableEnricher:

    def __init__(self, index_path: Path):
        with open(index_path, encoding="utf-8") as f:
            self.index = json.load(f)

    def get_raw(self, set_number: str) -> Dict[str, Any]:
        key = normalize_set_number(set_number)

        if key not in self.index:
            raise KeyError(f"[RB JOIN FAILED] Missing set_number: {key}")

        return self.index[key]

    def enrich(self, set_number: str) -> RebrickableData:
        key = normalize_set_number(set_number)
        data = self.get_raw(key)

        num_parts = data.get("num_parts")
        num_minifigs = data.get("num_minifigs")

        missing_parts = num_parts is None
        missing_minifigs = num_minifigs is None
        missing_theme = data.get("theme") is None

        return RebrickableData(
            name=data.get("name"),
            year=data.get("year"),
            theme=data.get("theme"),
            theme_family=data.get("theme_family"),
            theme_path=data.get("theme_path") or [],
            theme_depth=data.get("theme_depth"),
            num_parts=num_parts,
            num_minifigs=num_minifigs or 0,
            image_url=f"https://cdn.rebrickable.com/media/sets/{key}.jpg",
            retired_year=data.get("retired_year"),
            missing_parts=missing_parts,
            missing_minifigs=missing_minifigs,
            missing_theme=missing_theme,
            raw=data,
        )
