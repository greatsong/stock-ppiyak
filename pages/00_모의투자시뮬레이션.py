import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="모의 투자 시뮬레이션", page_icon="💰")

st.title("💰 모의 투자 시뮬레이션")
st.write("1년 전, 그 종목에 투자했다면 지금 얼마가 되어 있을까요?")

# 종목 이름 → 종목 코드로 바꿔 주는 표
종목표 = {
    "삼성전자": "005930.KS",
    "sk하이닉스": "000660.KS",
    "현대차": "005380.KS",
    "네이버": "035420.KS",
    "카카오": "035720.KS",
    "기아": "000270.KS",
    "셀트리온": "068270.KS",
    "애플": "AAPL",
    "테슬라": "TSLA",
    "엔비디아": "NVDA",
    "마이크로소프트": "MSFT",
    "구글": "GOOGL",
    "아마존": "AMZN",
}

이름 = st.text_input("종목 이름 (예: 삼성전자, 애플)", "삼성전자")
투자금 = st.number_input("투자할 금액 (원)", min_value=0, value=100000, step=100000)

if st.button("수익률 확인하기"):
    # 표에 있으면 코드로 바꾸고, 없으면 입력한 그대로 사용
    종목 = 종목표.get(이름.strip(), 이름.strip())

    데이터 = yf.download(종목, period="1y")

    if 데이터.empty:
        st.error("데이터를 가져오지 못했어요. 종목 이름을 다시 확인하거나, 잠시 후 다시 눌러 보세요.")
    else:
        시작가 = float(데이터["Close"].iloc[0])
        현재가 = float(데이터["Close"].iloc[-1])
        수익률 = (현재가 - 시작가) / 시작가 * 100
        평가금 = 투자금 * (현재가 / 시작가)

        st.metric("지금 내 평가금", f"{평가금:,.0f}원", f"{수익률:+.1f}%")

        그래프 = go.Figure()
        그래프.add_trace(go.Scatter(x=데이터.index, y=데이터["Close"], name="종가"))
        그래프.update_layout(title=f"{이름}의 1년 주가 변화", xaxis_title="날짜", yaxis_title="가격")
        st.plotly_chart(그래프)
