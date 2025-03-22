from enum import Enum

from typing import NamedTuple, List

class Candle(NamedTuple):
    timestamp: str
    open: str
    high: str
    low: str
    close: str
    volume: str

Candles = List[Candle]

class Sentiment(Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"