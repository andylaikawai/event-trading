from pydantic import BaseModel
from typing import List
from utils.util import format_time


class Candle(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    datetime: str

    @classmethod
    def from_ohlcv(cls, ohlcv: List[float]):
        timestamp = int(ohlcv[0])
        return cls(
            timestamp=timestamp,
            open=ohlcv[1],
            high=ohlcv[2],
            low=ohlcv[3],
            close=ohlcv[4],
            volume=ohlcv[5],
            datetime=format_time(timestamp)
        )

Candles = List[Candle]