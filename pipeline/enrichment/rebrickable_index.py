import json
from pathlib import Path
from typing import Dict, Any


def normalize_set_number(n: str) -> str:
    """
    Ensures set numbers are in canonical form: '1234-1'
    If the suffix is missing, append '-1'.
    """
    if not n:
        return ""

    n = str(n).strip()

    if "-" in n:
        return n

    return f"{n}-1"


class RebrickableIndex:
    """
    Wrapper around the RB index JSON file.
    Provides lookup, existence checks, and save functionality.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        with open(self.path, "r", encoding="utf-8") as f:
            self.index: Dict[str, Dict[str, Any]] = json.load(f)

    def lookup(self, set_number: str) -> Dict[str, Any] | None:
        key = normalize_set_number(set_number)
        return self.index.get(key)

    def has_set(self, set_number: str) -> bool:
        key = normalize_set_number(set_number)
        return key in self.index

    def add(self, data: Dict[str, Any]):
        """
        Adds a new RB entry to the index.
        Expects data['set_num'] or data['set_number'] to exist.
        """
        key = normalize_set_number(
            data.get("set_num") or data.get("set_number")
        )
        self.index[key] = data

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.index, f, indent=2)
