# canonical/helpers/completeness.py

import re

def infer_completeness(title: str):
    """
    Infer completeness and component flags from the listing title.
    Returns:
        completeness: str | None
        has_minifigs: bool
        has_box: bool
        has_instructions: bool
    """
    t = (title or "").lower()

    has_minifigs = any(word in t for word in ["minifig", "minifigs", "figs"])
    has_box = "box" in t
    has_instructions = any(word in t for word in ["manual", "instructions", "booklet"])

    # completeness classification
    if "minifig" in t and "only" in t:
        completeness = "minifigs_only"
    elif "complete" in t:
        completeness = "complete"
    elif "incomplete" in t:
        completeness = "incomplete"
    else:
        completeness = None

    return completeness, has_minifigs, has_box, has_instructions
