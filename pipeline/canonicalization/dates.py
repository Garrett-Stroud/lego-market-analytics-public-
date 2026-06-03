# canonical/helpers/dates.py

from datetime import datetime

def parse_sold_timestamp(date_str: str) -> int:
    """
    Convert a extraction date string into a Unix timestamp.
    Supports multiple formats.
    """
    if not date_str:
        return int(datetime.utcnow().timestamp())

    formats = [
        "%b-%d-%y",     # May-28-24
        "%Y-%m-%d",     # 2024-05-28
        "%m/%d/%Y",     # 05/28/2024
        "%d %b %Y",     # 28 May 2024
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return int(dt.timestamp())
        except Exception:
            pass

    # fallback: now
    return int(datetime.utcnow().timestamp())
