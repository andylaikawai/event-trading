import logging
from typing import Tuple, Optional

import ccxt

from config import KUCOIN_API_KEY, KUCOIN_SECRET, KUCOIN_PASSPHRASE, LOOK_BACK_PERIOD, MAX_OBSERVATION_PERIOD, \
    MAX_HOLDING_PERIOD
from model.candles import Candles, Candle
from utils.util import min_to_ms

# Initialize exchange
exchange = ccxt.kucoin({
    # 'apiKey': KUCOIN_API_KEY,
    # 'secret': KUCOIN_SECRET,
    # 'password': KUCOIN_PASSPHRASE,
    'enableRateLimit': True,
})


def fetch_candles_from_exchange(symbol: str, from_timestamp: int, to_timestamp: int = None,
                                number_of_candles: int = None) -> Optional[Candles]:
    params = {
        'paginate': True,
        'since': from_timestamp,
        'until': to_timestamp,
        'paginationCalls': 100
    }
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m', since=from_timestamp,
                                 limit=number_of_candles, params=params)
    return [Candle.from_ohlcv(candle) for candle in ohlcv]


def fetch_relevant_candles(symbol: str, timestamp: int) -> Tuple[
    Optional[Candles], Optional[Candles], Optional[Candles]]:
    number_of_candles = LOOK_BACK_PERIOD + MAX_OBSERVATION_PERIOD + MAX_HOLDING_PERIOD
    start_candle_timestamp = timestamp - min_to_ms(LOOK_BACK_PERIOD)
    end_candle_timestamp = timestamp + min_to_ms(MAX_OBSERVATION_PERIOD + MAX_HOLDING_PERIOD)

    try:
        # TODO use to_timestamp params instead
        candles = fetch_candles_from_exchange(f"{symbol}/USDT", from_timestamp=start_candle_timestamp, number_of_candles=number_of_candles)

        # Split candles into previous/current for sentiment analysis and future for performance evaluation
        # TODO this is backtest specific
        observe_until = timestamp + min_to_ms(MAX_OBSERVATION_PERIOD)
        previous_candles = [candle for candle in candles if candle.timestamp <= timestamp]
        observation_candles = [candle for candle in candles if timestamp < candle.timestamp <= observe_until]
        performance_candles = [candle for candle in candles if candle.timestamp > observe_until]

        return previous_candles, observation_candles, performance_candles

    except Exception as e:
        logging.debug(f"[ERROR] Failed to fetch market price: {e}")
        return None, None, None

