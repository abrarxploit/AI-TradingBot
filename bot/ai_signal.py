import pandas as pd

def calculate_rsi(prices, period=14):
    delta = pd.Series(prices).diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def get_signal(prices):
    rsi = calculate_rsi(prices)

    last_rsi = rsi.iloc[-1]

    if last_rsi < 30:
        return "BUY"
    elif last_rsi > 70:
        return "SELL"
    else:
        return "HOLD"