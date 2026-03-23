import logging
import pandas as pd
from pykrx import stock as krx
from config import BACKUP_CSV_PATH, UNIVERSE_MIN_COUNT
from utils import is_excluded_by_text, to_date_str

def get_universe(target_date):
    date_str = to_date_str(target_date)
    try:
        cap_df = krx.get_market_cap_by_ticker(date_str)
        if cap_df is None or cap_df.empty: return load_backup()
        
        market_map = {}
        for m in ["KOSPI", "KOSDAQ"]:
            for t in krx.get_market_ticker_list(date_str, market=m):
                market_map[t] = m
        
        rows = []
        for ticker, market in market_map.items():
            name = krx.get_market_ticker_name(ticker)
            rows.append({
                "ticker": ticker, "name": name, "market": market,
                "market_cap": cap_df.loc[ticker, "시가총액"] if ticker in cap_df.index else 0
            })
        df = pd.DataFrame(rows)
        df.to_csv(BACKUP_CSV_PATH, index=False, encoding="utf-8-sig")
        return df
    except:
        return load_backup()

def load_backup():
    if not BACKUP_CSV_PATH.exists(): return None
    return pd.read_csv(BACKUP_CSV_PATH, dtype={"ticker": str})

def apply_text_filter(df):
    mask = df["name"].apply(is_excluded_by_text)
    return df[~mask].copy().reset_index(drop=True), int(mask.sum())
