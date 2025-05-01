from dataclasses import dataclass
from typing import List, Optional

from model.candles import Candles, Candle
from utils.util import format_time


@dataclass
class NewsEvent:
    title: Optional[str]
    time: int
    url: Optional[str]
    source: Optional[str]
    suggestions: Optional[List[dict]]
    message: Optional[str]
    user: Optional[dict]
    datetime: str

    @staticmethod
    def from_dict(data: dict):
        timestamp = data.get("time", 0)
        return NewsEvent(
            title=data.get("title"),
            time=timestamp, # TODO rename to timestamp
            url=data.get("url") or data.get("link"),
            source=data.get("source"),
            suggestions=data.get("suggestions"),
            message=data.get("message"), # TODO: for login ws message only, consider remove / remodel
            user=data.get("user"), # TODO: for login ws message only, consider remove / remodel
            datetime = format_time(timestamp)
        )

@dataclass
class HistoricalNewsEvent(NewsEvent):
    previous_candles: Candles
    observation_candles: Candles
    performance_candle: Candle

    @staticmethod
    def from_dict(data: dict):
        timestamp = data.get("time", 0)
        return HistoricalNewsEvent(
            title=data.get("title"),
            time=timestamp,
            url=data.get("url"),
            source=data.get("source"),
            suggestions=data.get("suggestions"),
            message=data.get("message"),
            user=data.get("user"),
            datetime=format_time(timestamp),
            previous_candles=[Candle.from_ohlcv(c) for c in data.get("previous_candles")],
            observation_candles=[Candle.from_ohlcv(c) for c in data.get("observation_candles")],
            performance_candle=Candle.from_ohlcv(data.get("performance_candle"))
        )