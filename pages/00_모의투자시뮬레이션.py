import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("💰 모의 투자 시뮬레이션")
st.write("1년 전, 그 종목에 투자했다면 지금 얼마가 되어 있을까요?")

종목 = st.text_input("종목 코드 (예: 삼성전자 005930.KS, 애플 AAPL)", "005930.KS")
투자금 = st.number_input("투자할 금액 (원)", min_value=0, value=100000, step=100000)

if st.button("수익률 확인하기"):
    데이터 = yf.download(종목, period="1y")
    시작가 = float(데이터["Close"].iloc[0])
    현재가 = float(데이터["Close"].iloc[-1])
    수익률 = (현재가 - 시작가) / 시작가 * 100
    평가금 = 투자금 * (현재가 / 시작가)

    st.metric("지금 내 평가금", f"{평가금:,.0f}원", f"{수익률:+.1f}%")

    그래프 = go.Figure()
    그래프.add_trace(go.Scatter(x=데이터.index, y=데이터["Close"], name="종가"))
    그래프.update_layout(title=f"{종목}의 1년 주가 변화", xaxis_title="날짜", yaxis_title="가격")
    st.plotly_chart(그래프)
