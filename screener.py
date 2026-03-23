import time
import pandas as pd
from pykrx import stock as krx
from config import *
from utils import date_range_lookback, format_억, format_pct, to_date_str

def run_screener(univ_df, target_date):
    d_str = to_date_str(target_date)
    # 당일 전종목 데이터 한 번에 가져오기
    snap = krx.get_market_ohlcv_by_ticker(d_str)
    if snap is None or snap.empty:
        return pd.DataFrame(), {}

    results = []
    counts = {Status.LOW_MARKET_CAP: 0, Status.LOW_VALUE_TODAY: 0, Status.PASSED: 0}

    # 1단계: 시총과 당일 거래대금으로 1차 필터링
    precut = []
    for r in univ_df.itertuples():
        if r.market_cap < MIN_MARKET_CAP:
            counts[Status.LOW_MARKET_CAP] += 1
            continue
        if r.ticker not in snap.index: continue
        
        val = snap.loc[r.ticker, "거래대금"]
        if val < MIN_VOLUME_TODAY:
            counts[Status.LOW_VALUE_TODAY] += 1
            continue
            
        precut.append((r.ticker, r.name, r.market, val))

    # 2단계: 1차 통과한 종목들만 정밀 분석
    print(f"상세 분석 대상: {len(precut)} 종목...")
    for t, n, m, v in precut:
        try:
            s, e = date_range_lookback(target_date, 200)
            df = krx.get_market_ohlcv_by_date(s, e, t)
            time.sleep(0.05) # 서버 차단 방지용 미세 지연

            if df is None or len(df) < MIN_DATA_DAYS: continue
            
            # 수급(TV배수) 계산
            v_20 = df["거래대금"].iloc[-20:].mean()
            tv = v / v_20 if v_20 > 0 else 0
            if tv < MIN_TV_RATIO: continue

            # 수익률 계산
            close = df["종가"]
            day_ret = (close.iloc[-1] / close.iloc[-2]) - 1
            
            results.append({
                "ticker": t, "name": n, "market": m, 
                "당일수익률(%)": format_pct(day_ret),
                "당일거래대금(억)": format_억(v), 
                "TV배수": round(tv, 2), "태그": "통과"
            })
        except: continue

    res_df = pd.DataFrame(results).sort_values("당일수익률(%)", ascending=False) if results else pd.DataFrame()
    counts[Status.PASSED] = len(res_df)
    return res_df, counts
