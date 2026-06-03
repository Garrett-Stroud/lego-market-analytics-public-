from datetime import datetime

def iso_to_timestamp(iso_str: str) -> int:
    if not iso_str:
        return None
    try:
        return int(datetime.fromisoformat(iso_str.replace("Z", "")).timestamp())
    except:
        return None
