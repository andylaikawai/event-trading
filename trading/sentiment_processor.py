import logging
from typing import Union, Optional, Tuple

from backtest.back_test import paper_trade
from config import IS_BACKTEST_MODE, MAX_OBSERVATION_PERIOD, MAX_HOLDING_PERIOD, LOOK_BACK_PERIOD
from trading.exchange import exchange
from trading.trade_executor import live_trade
from type.type import Sentiment, Candles, Candle


def execute_trade_based_on_signals(symbol: str, timestamp: int) -> Optional[float]:
    previous_candle, observation_candles, performance_candles = _fetch_market_price(symbol, timestamp)
    sentiment = _get_sentiment(symbol, previous_candle, observation_candles)
    _make_trade(symbol, sentiment, observation_candles[-1], performance_candles)
    return _detect_price_movement(performance_candles)


def _make_trade(symbol: str, sentiment: Sentiment, candle: Candle, performance_candles: Candles):
    trade_executor = paper_trade if IS_BACKTEST_MODE else live_trade
    trade_executor(symbol, sentiment, candle, performance_candles)


def _get_sentiment(symbol: str, previous_candles: Candles, obsevation_candles: Candles) -> Sentiment:
    if previous_candles is None or obsevation_candles is None:
        return Sentiment.NEUTRAL

    first_candle = previous_candles[0]
    current_candle = obsevation_candles[-1]
    previous_close = float(first_candle.close)
    current_close = float(current_candle.close)

    if current_close > previous_close * 1.001:
        logging.debug(f"[TRADE] Positive sentiment detected for {symbol}.")
        return Sentiment.POSITIVE
    elif current_close < previous_close * 0.999:
        logging.debug(f"[TRADE] Negative sentiment detected for {symbol}.")
        return Sentiment.NEGATIVE
    else:
        return Sentiment.NEUTRAL

def _min_to_ms(min: int) -> int:
    return min * 60 * 1000

def _fetch_market_price(symbol: str, timestamp: int) -> Tuple[Optional[Candles], Optional[Candles], Optional[Candles]]:
    try:
        number_of_candles = LOOK_BACK_PERIOD + MAX_OBSERVATION_PERIOD + MAX_HOLDING_PERIOD
        start_candle_timestamp = timestamp - _min_to_ms(LOOK_BACK_PERIOD)
        ohlcv = exchange.fetch_ohlcv(f"{symbol}/USDT", timeframe='1m', since=start_candle_timestamp, limit=number_of_candles)
        candles = [Candle.from_ohlcv(candle) for candle in ohlcv]

        # Split candles into previous/current for sentiment analysis and future for performance evaluation
        # TODO this is backtest specific
        observe_until = timestamp + _min_to_ms(MAX_OBSERVATION_PERIOD)
        previous_candles = [candle for candle in candles if candle.timestamp <= timestamp]
        observation_candles = [candle for candle in candles if timestamp < candle.timestamp <= observe_until]
        performance_candles = [candle for candle in candles if candle.timestamp > observe_until]

        return previous_candles, observation_candles, performance_candles

    except Exception as e:
        logging.error(f"[ERROR] Failed to fetch market price: {e}")
        return None, None, None


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
