# canonical/helpers/seller.py

import re

def parse_seller_block(text: str):
    """
    Extract seller username, feedback %, and feedback count
    from raw seller block text.
    """
    if not text:
        return None, None, None

    m = re.search(r"([A-Za-z0-9_-]+)\s+(\d+)% positive \((\d+)\)", text)
    if not m:
        return None, None, None

    username = m.group(1)
    pct = int(m.group(2))
    count = int(m.group(3))

    return username, pct, count
