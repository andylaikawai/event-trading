from typing import Optional

from config import SYMBOL, RAW_CANDLES_FILE
from model.candles import Candles, Candle
from trading.exchange import fetch_candles_from_exchange
from utils.util import read_from_cache_or_fetch


def get_candles(from_timestamp: int, to_timestamp: int) -> Optional[Candles]:
    ohlcv = read_from_cache_or_fetch(RAW_CANDLES_FILE, fetch_candles_from_exchange, f"{SYMBOL}/USDT", from_timestamp,
                                     to_timestamp)
    return [Candle.from_ohlcv(candle) for candle in ohlcv]
