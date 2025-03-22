from datetime import datetime, timezone
from enum import Enum

from typing import NamedTuple, List

class Candle(NamedTuple):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    datetime: str

    @staticmethod
    def from_ohlcv(ohlcv):
        timestamp = ohlcv[0]
        return Candle(
            timestamp=timestamp,
            open=ohlcv[1],
            high=ohlcv[2],
            low=ohlcv[3],
            close=ohlcv[4],
            volume=ohlcv[5],
            datetime=datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        )

Candles = List[Candle]

class Sentiment(Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"