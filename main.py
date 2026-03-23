import sys
import logging
from datetime import date, datetime
import pandas as pd
from pykrx import stock as krx
from config import OUTPUT_DIR, OUTPUT_COLUMNS, Status
from universe import get_universe, apply_text_filter

logging.basicConfig(level=logging.INFO, format="%(message)s")

def main():
    target_date = date.today()
    if len(sys.argv) > 2 and sys.argv[1] == "--date":
        target_date = datetime.strptime(sys.argv[2], "%Y%m%d").date()
    
    print(f"\n[작업 시작] 기준일: {target_date}")
    
    univ = get_universe(target_date)
    if univ is None:
        print("데이터를 가져올 수 없습니다. 날짜를 확인하세요."); return

    filtered_univ, n_text = apply_text_filter(univ)
    # 실제 스크리닝 로직은 screener.py에 있으나, 테스트를 위해 간단히 출력
    print(f"유니버스 확보: {len(univ)}개 / 필터 제거: {n_text}개")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("\n설정이 완료되었습니다! 이제 터미널에서 실행해 보세요.")

if __name__ == "__main__":
    main()
