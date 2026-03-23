from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
BACKUP_CSV_PATH = BASE_DIR / "krx_universe_backup.csv"

UNIVERSE_MIN_COUNT = 1000
OHLCV_LOOKBACK_CALENDAR_DAYS = 200

MIN_MARKET_CAP = 100_000_000_000
MIN_DATA_DAYS = 60
MIN_VOLUME_TODAY = 10_000_000_000
MIN_VOLUME_5D_AVG = 3_000_000_000
MIN_TV_RATIO = 1.2
MIN_POSITION_20D = 0.82
MAX_OVERHEAT_MA20 = 1.30

TV_SPIKE_HIGH = 2.0
TV_SPIKE_NEW = 3.0
TV_SPIKE_MID = 1.5

EXCLUDE_KEYWORDS = ["KODEX", "TIGER", "KBSTAR", "RISE", "ACE", "ARIRANG", "PLUS", "ETN", "스팩", "SPAC", "리츠", "REIT"]
PREFERRED_STOCK_SUFFIXES = ["우B", "우C", "1우", "2우", "3우", "우"]

CONSOLE_TOP_N = 30
OUTPUT_COLUMNS = ["ticker", "name", "market", "당일수익률(%)", "당일거래대금(억)", "TV배수", "태그"]

class Status:
    FILTERED_TEXT = "filtered_text"
    TOO_SHORT = "too_short"
    LOW_MARKET_CAP = "low_market_cap"
    LOW_VALUE_TODAY = "low_value_today"
    LOW_VALUE_5D = "low_value_5d"
    LOW_SPIKE = "low_spike"
    LOW_POSITION_20D = "low_position_20d"
    TOO_FAR_FROM_MA20 = "too_far_from_ma20"
    PASSED = "passed"
    EXCEPTION = "exception"
