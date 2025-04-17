from datetime import datetime
from typing import Optional

def parse_datetime(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except Exception:
        try:
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except Exception:
            return None

def parse_date(value: str) -> Optional[datetime.date]:
    dt = parse_datetime(value)
    return dt.date() if dt else None

def parse_float(value: str) -> Optional[float]:
    try:
        return float(str(value).replace(",", "."))
    except Exception:
        return None

def parse_int(value) -> Optional[int]:
    try:
        return int(value)
    except Exception:
        return None

def normalize_string(text) -> Optional[str]:
    return text.strip().upper() if isinstance(text, str) else text

def parse_bool(value) -> bool:
    return str(value).lower() in ("true", "1", "yes", "sim")
