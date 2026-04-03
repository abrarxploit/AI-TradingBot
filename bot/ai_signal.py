import logging
import pandas as pd

logger = logging.getLogger(__name__)

RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70


def calculate_rsi(prices: list, period: int = RSI_PERIOD) -> pd.Series:
    """
    Calculate RSI for a list of closing prices.

    Args:
        prices: List of closing prices (float)
        period: RSI lookback period (default 14)

    Returns:
        pandas Series of RSI values

    Raises:
        ValueError: if not enough prices are provided
    """
    if len(prices) < period + 1:
        raise ValueError(
            f"Need at least {period + 1} prices to calculate RSI, got {len(prices)}. "
            f"Increase the klines limit."
        )

    series = pd.Series(prices)
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    # Avoid division by zero (pure uptrend scenario → RSI = 100)
    avg_loss = avg_loss.replace(0, 1e-10)

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    logger.debug("RSI calculated — last value: %.2f", rsi.iloc[-1])
    return rsi


def get_signal(prices: list) -> str:
    """
    Generate a BUY / SELL / HOLD signal based on RSI.

    Args:
        prices: List of closing prices

    Returns:
        "BUY", "SELL", or "HOLD"
    """
    try:
        rsi = calculate_rsi(prices)
    except ValueError as e:
        logger.warning("RSI calculation failed: %s — defaulting to HOLD", e)
        return "HOLD"

    last_rsi = rsi.iloc[-1]

    if pd.isna(last_rsi):
        logger.warning("RSI returned NaN — not enough data, defaulting to HOLD")
        return "HOLD"

    logger.info("RSI signal — value=%.2f threshold_low=%s threshold_high=%s",
                last_rsi, RSI_OVERSOLD, RSI_OVERBOUGHT)

    if last_rsi < RSI_OVERSOLD:
        signal = "BUY"
    elif last_rsi > RSI_OVERBOUGHT:
        signal = "SELL"
    else:
        signal = "HOLD"

    logger.info("Signal generated: %s", signal)
    return signal
