import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import plotly.graph_objs as go

st.set_page_config(page_title="RSI 다이버전스 트레이딩", page_icon="📈")
st.title("📈 RSI 다이버전스 트레이딩")

symbol = st.sidebar.text_input("종목 코드 입력 (예: AAPL, 005930.KS)", value="AAPL")
start_date = st.sidebar.date_input("시작 날짜", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("종료 날짜", pd.to_datetime("2024-04-01"))

data = yf.download(symbol, start=start_date, end=end_date)
if data.empty or 'Close' not in data.columns:
    st.error("❌ 데이터를 가져오지 못했습니다.")
    st.stop()

data['RSI'] = ta.momentum.RSIIndicator(close=data['Close'], window=14).rsi()

def find_bullish_divergence(df):
    points = []
    for i in range(30, len(df)):
        if df['Close'].iloc[i] < df['Close'].iloc[i-10:i].min() and df['RSI'].iloc[i] > df['RSI'].iloc[i-10:i].min():
            points.append(i)
    return points

def find_bearish_divergence(df):
    points = []
    for i in range(30, len(df)):
        if df['Close'].iloc[i] > df['Close'].iloc[i-10:i].max() and df['RSI'].iloc[i] < df['RSI'].iloc[i-10:i].max():
            points.append(i)
    return points

bullish = find_bullish_divergence(data)
bearish = find_bearish_divergence(data)

# 가격 차트
fig_price = go.Figure()
fig_price.add_trace(go.Scatter(x=data.index, y=data['Close'], name="종가", line=dict(color="blue"))
fig_price.add_trace(go.Scatter(x=data.index[bullish], y=data['Close'].iloc[bullish], mode='markers', name='🟢 매수', marker=dict(color='green', size=10)))
fig_price.add_trace(go.Scatter(x=data.index[bearish], y=data['Close'].iloc[bearish], mode='markers', name='🔴 매도', marker=dict(color='red', size=10)))
fig_price.update_layout(title=f"{symbol} 가격 및 RSI 다이버전스", xaxis_title="날짜", yaxis_title="가격")
st.plotly_chart(fig_price, use_container_width=True)

# RSI 차트
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=data.index, y=data['RSI'], name="RSI", line=dict(color="purple")))
fig_rsi.add_hline(y=70, line=dict(color="gray", dash="dot"))
fig_rsi.add_hline(y=30, line=dict(color="gray", dash="dot"))
fig_rsi.update_layout(title="RSI 지표", xaxis_title="날짜", yaxis_title="RSI")
st.plotly_chart(fig_rsi, use_container_width=True)
