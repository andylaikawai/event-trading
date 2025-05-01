from functools import reduce
from typing import Union, Optional, Tuple

from backtest.back_test import paper_trade
from config import IS_BACKTEST_MODE
from trading.trade_executor import live_trade
from model.candles import Candles, Candle
from model.sentiment import Sentiment


def execute_trade_based_on_sentiment(symbol: str, sentiment, candle: Candle, performance_candles) -> Optional[float]:
    _make_trade(symbol, sentiment, candle, performance_candles)
    return _detect_price_movement(performance_candles)


def _make_trade(symbol: str, sentiment: Sentiment, candle: Candle, performance_candles: Candles):
    trade_executor = paper_trade if IS_BACKTEST_MODE else live_trade
    trade_executor(symbol, sentiment, candle, performance_candles)


def _detect_price_movement(candles: Candles) -> Union[float, None]:
    """Detect if the market price moved by more than 2%."""
    if candles is None or len(candles) < 2:
        return None

    initial_price = candles[0].close
    final_price = candles[-1].close

    price_change = (final_price - initial_price) / initial_price

    abs_price_change = abs(price_change)
    if abs_price_change > 0.02:
        return price_change * 100

    return None
