import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="주가 1년 변화", page_icon="📈", layout="wide")

st.title("📈 주식 1년 주가 변화")
st.caption("종목 이름을 입력하고 버튼을 누르면 최근 1년 주가를 보여줍니다.")

# 자주 쓰는 종목명 → 티커 매핑 (한글/영문 모두 지원)
TICKER_MAP = {
    "삼성전자": "005930.KS",
    "sk하이닉스": "000660.KS",
    "현대차": "005380.KS",
    "네이버": "035420.KS",
    "naver": "035420.KS",
    "카카오": "035720.KS",
    "lg에너지솔루션": "373220.KS",
    "삼성바이오로직스": "207940.KS",
    "기아": "000270.KS",
    "포스코홀딩스": "005490.KS",
    "셀트리온": "068270.KS",
    "애플": "AAPL",
    "apple": "AAPL",
    "테슬라": "TSLA",
    "tesla": "TSLA",
    "엔비디아": "NVDA",
    "nvidia": "NVDA",
    "마이크로소프트": "MSFT",
    "microsoft": "MSFT",
    "구글": "GOOGL",
    "google": "GOOGL",
    "아마존": "AMZN",
    "amazon": "AMZN",
    "메타": "META",
    "meta": "META",
}


def resolve_ticker(name: str) -> str:
    """입력한 이름을 티커로 변환. 매핑에 없으면 입력값을 그대로 티커로 사용."""
    key = name.strip().lower()
    return TICKER_MAP.get(key, name.strip().upper())


name = st.text_input("주식 종목 이름", placeholder="예: 삼성전자, 애플, AAPL")

if st.button("주가 가져오기", type="primary"):
    if not name.strip():
        st.warning("종목 이름을 입력해 주세요.")
    else:
        ticker = resolve_ticker(name)
        with st.spinner(f"'{name}' ({ticker}) 데이터를 가져오는 중..."):
            end = datetime.now()
            start = end - timedelta(days=365)
            df = yf.download(ticker, start=start, end=end, progress=False)

        if df.empty:
            st.error(
                f"'{name}' 데이터를 찾을 수 없습니다. "
                "정확한 종목명이나 티커(예: AAPL, 005930.KS)를 입력해 보세요."
            )
        else:
            # 컬럼이 MultiIndex로 올 때 평탄화
            if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
                df.columns = df.columns.get_level_values(0)

            close = df["Close"]
            first_price = float(close.iloc[0])
            last_price = float(close.iloc[-1])
            change_pct = (last_price - first_price) / first_price * 100

            c1, c2, c3 = st.columns(3)
            c1.metric("현재가", f"{last_price:,.2f}")
            c2.metric("1년 전", f"{first_price:,.2f}")
            c3.metric("변화율", f"{change_pct:+.2f}%")

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=close,
                    mode="lines",
                    name="종가",
                    line=dict(color="#2E86DE", width=2),
                )
            )
            fig.update_layout(
                title=f"{name} ({ticker}) 최근 1년 주가",
                xaxis_title="날짜",
                yaxis_title="종가",
                hovermode="x unified",
                template="plotly_white",
                height=500,
            )
            st.plotly_chart(fig, use_container_width=True)
