import re
from typing import Optional, List
from rapidfuzz import fuzz

class SetNumberExtractor:
    """
    Production-grade LEGO set-number extractor.
    Uses multi-candidate scoring with RB index validation.
    """

    def __init__(self, rb_index: dict):
        self.rb_index = rb_index

    def extract(self, title: str, piece_count: Optional[int] = None) -> Optional[str]:
        candidates = self._extract_numeric_candidates(title)
        if not candidates:
            return None

        scored = []
        for raw in candidates:
            canonical = f"{raw}-1"
            if canonical not in self.rb_index:
                continue

            score = self._score_candidate(canonical, title, piece_count)
            scored.append((canonical, score))

        if not scored:
            return None

        best, best_score = max(scored, key=lambda x: x[1])
        if best_score < 40:
            return None

        return best

    def _extract_numeric_candidates(self, text: str) -> List[str]:
        nums = re.findall(r"\b(\d{3,6})\b", text)
        seen = set()
        out = []
        for n in nums:
            if n not in seen:
                seen.add(n)
                out.append(n)
        return out

    def _score_candidate(self, set_num: str, title: str, piece_count: Optional[int]) -> float:
        rb = self.rb_index.get(set_num)
        if not rb:
            return 0

        score = 0.0

        rb_name = rb.get("name") or ""
        score += fuzz.partial_ratio(title.lower(), rb_name.lower()) * 0.6

        theme = rb.get("theme") or ""
        if theme.lower() in title.lower():
            score += 15

        family = rb.get("theme_family") or ""
        if family.lower() in title.lower():
            score += 10

        rb_parts = rb.get("num_parts")
        if piece_count and rb_parts:
            diff = abs(piece_count - rb_parts)
            if diff < 50:
                score += 20
            elif diff < 200:
                score += 10

        year = rb.get("year")
        if year and year > 2000:
            score += 5

        return score
