import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt

# 종목 불러오기
symbol = "012450.KS"
data = yf.download(symbol, start="2023-01-01", end="2025-04-03")

# RSI 계산
close = data['Close'].squeeze()
data['RSI'] = ta.momentum.RSIIndicator(close=close, window=14).rsi().squeeze()

# 불리쉬 다이버전스 (매수)
def find_bullish_divergence(df):
    divergences = []
    for i in range(30, len(df)):
        price_now = float(df['Close'].iloc[i])
        price_prev = float(df['Close'].iloc[i-10:i].min())
        rsi_now = float(df['RSI'].iloc[i])
        rsi_prev = float(df['RSI'].iloc[i-10:i].min())
        if price_now < price_prev and rsi_now > rsi_prev:
            divergences.append(i)
    return divergences

# 베어리쉬 다이버전스 (매도)
def find_bearish_divergence(df):
    divergences = []
    for i in range(30, len(df)):
        price_now = float(df['Close'].iloc[i])
        price_prev = float(df['Close'].iloc[i-10:i].max())
        rsi_now = float(df['RSI'].iloc[i])
        rsi_prev = float(df['RSI'].iloc[i-10:i].max())
        if price_now > price_prev and rsi_now < rsi_prev:
            divergences.append(i)
    return divergences

# 📍 시그널 포착
bullish_points = find_bullish_divergence(data)
bearish_points = find_bearish_divergence(data)

# 📊 시각화
plt.figure(figsize=(14, 7))

# 📈 가격 차트
plt.subplot(2, 1, 1)
plt.plot(data['Close'], label='Close Price')
plt.scatter(data.iloc[bullish_points].index, data['Close'].iloc[bullish_points], color='green', label='Bullish Divergence')  # 매수
plt.scatter(data.iloc[bearish_points].index, data['Close'].iloc[bearish_points], color='red', label='Bearish Divergence')    # 매도
plt.legend()
plt.title(f'{symbol} Price with RSI Divergence Signals')

# 📉 RSI 차트
plt.subplot(2, 1, 2)
plt.plot(data['RSI'], label='RSI', color='purple')
plt.axhline(30, color='gray', linestyle='--')
plt.axhline(70, color='gray', linestyle='--')
plt.legend()

plt.tight_layout()
plt.show()
