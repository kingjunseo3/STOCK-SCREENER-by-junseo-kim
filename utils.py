from datetime import date, timedelta
from config import EXCLUDE_KEYWORDS, PREFERRED_STOCK_SUFFIXES

def is_excluded_by_text(name: str):
    if not name: return True
    upper_name = name.upper()
    if any(kw in upper_name for kw in EXCLUDE_KEYWORDS): return True
    for suffix in sorted(PREFERRED_STOCK_SUFFIXES, key=len, reverse=True):
        if name.endswith(suffix): return True
    return False

def to_date_str(d: date): return d.strftime("%Y%m%d")

def date_range_lookback(target_date: date, days: int):
    start = target_date - timedelta(days=days)
    return to_date_str(start), to_date_str(target_date)

def format_억(val: float): return round(val / 100_000_000, 1)
def format_pct(val: float): return round(val * 100, 2)
