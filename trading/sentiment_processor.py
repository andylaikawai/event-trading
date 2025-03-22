import logging
from typing import Union

from backtest.back_test import paper_trade
from config import DEFAULT_TRADE_AMOUNT, IS_BACKTEST_MODE
from trading.exchange import exchange
from trading.trade_executor import live_trade
from type.type import Sentiment, Candles, Candle


def execute_trade_based_on_signals(symbol: str, timestamp: int) -> bool:
    candles = _fetch_market_price(symbol, timestamp)
    sentiment = _get_sentiment(symbol, candles)
    _make_trade(symbol, sentiment)
    return _detect_price_movement(candles)


def _make_trade(symbol: str, sentiment: Sentiment):
    trade_amount = DEFAULT_TRADE_AMOUNT
    trade_executor = paper_trade if IS_BACKTEST_MODE else live_trade
    trade_executor(symbol, trade_amount, sentiment)


def _get_sentiment(symbol: str, candles: Union[Candles, None]) -> Sentiment:
    if candles is None:
        return Sentiment.NEUTRAL

    first_candle = candles[0]
    last_candle = candles[-1]
    previous_close = float(first_candle.close)
    current_close = float(last_candle.close)

    if current_close > previous_close * 1.001:
        logging.debug(f"[TRADE] Positive sentiment detected for {symbol}.")
        return Sentiment.POSITIVE
    elif current_close < previous_close * 0.999:
        logging.debug(f"[TRADE] Negative sentiment detected for {symbol}.")
        return Sentiment.NEGATIVE
    else:
        return Sentiment.NEUTRAL


def _fetch_market_price(symbol: str, timestamp: int) -> Union[Candles, None]:
    """Fetch the market price from KuCoin at a specific timestamp using ccxt."""
    try:
        # Convert timestamp to seconds
        timestamp_seconds = timestamp / 1000
        start_time = int(timestamp_seconds - 120) * 1000  # 2 minutes before the news timestamp in milliseconds

        # Fetch historical market data with a 1-minute interval
        ohlcv = exchange.fetch_ohlcv(f"{symbol}/USDT", timeframe='1m', since=start_time, limit=32)

        return [Candle.from_ohlcv(candle) for candle in ohlcv]

    except Exception as e:
        logging.error(f"[ERROR] Failed to fetch market price: {e}")
        return None


def _detect_price_movement(candles: Candles) -> Union[float, None]:
    """Detect if the market price moved by more than 2%."""
    if candles is None or len(candles) < 2:
        return None

    initial_price = candles[0].close
    final_price = candles[-1].close

    price_change = (final_price - initial_price) / initial_price

    abs_price_change = abs(price_change)
    if abs_price_change > 0.02:
        return price_change

    return None
