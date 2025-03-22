import logging
from typing import Union

from ccxt.static_dependencies.toolz import first

from backtest.back_test import paper_trade
from config import DEFAULT_TRADE_AMOUNT, is_backtest_mode
from trading.exchange import exchange
from trading.trade_executor import live_trade
from type.type import Sentiment, Candles, Candle


def execute_trade_based_on_signals(symbol: str, timestamp: int):
    sentiment = _get_sentiment(symbol, timestamp)
    _make_trade(symbol, sentiment)


def _make_trade(symbol: str, sentiment: Sentiment):
    trade_amount = DEFAULT_TRADE_AMOUNT
    trade_executor = paper_trade if is_backtest_mode else live_trade
    trade_executor(symbol, trade_amount, sentiment)


def _get_sentiment(symbol: str, timestamp: int) -> Sentiment:
    candles = _fetch_market_price(symbol, timestamp)
    if candles is None:
        return Sentiment.NEUTRAL

    first_candle = candles[0]
    last_candle = candles[-1]
    previous_close = float(first_candle[2])
    current_close = float(last_candle[2])

    if current_close > previous_close * 1.001:
        logging.info(f"[TRADE] Positive sentiment detected for {symbol}.")
        return Sentiment.POSITIVE
    elif current_close < previous_close * 0.999:
        logging.info(f"[TRADE] Negative sentiment detected for {symbol}.")
        return Sentiment.NEGATIVE
    else:
        return Sentiment.NEUTRAL


def _fetch_market_price(symbol: str, timestamp: int) -> Union[Candles, None]:
    """Fetch the market price from KuCoin at a specific timestamp using ccxt."""
    try:
        # Convert timestamp to seconds
        timestamp_seconds = timestamp / 1000
        start_time = int(timestamp_seconds - 120) * 1000  # 2 minutes before the news timestamp in milliseconds
        end_time = int(timestamp_seconds) * 1000  # At the news timestamp in milliseconds

        # Fetch historical market data with a 1-minute interval
        ohlcv = exchange.fetch_ohlcv(f"{symbol}/USDT", timeframe='1m', since=start_time, limit=2)

        return [
            Candle(
                timestamp=str(candle[0]),
                open=str(candle[1]),
                high=str(candle[2]),
                low=str(candle[3]),
                close=str(candle[4]),
                volume=str(candle[5])
            ) for candle in ohlcv
        ]

    except Exception as e:
        logging.error(f"Failed to fetch market price: {e}")
        return None
