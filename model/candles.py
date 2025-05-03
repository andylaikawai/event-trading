from dataclasses import dataclass
from typing import List

from utils.util import format_time


@dataclass
class Candle():
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
            datetime=format_time(timestamp)
        )

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume
        }

Candles = List[Candle]