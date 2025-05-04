from typing import Optional

from pydantic import BaseModel

from model.candles import Candles
from utils.util import format_time


class NewsEvent(BaseModel):
    title: Optional[str]
    timestamp: int
    url: Optional[str]
    source: Optional[str]
    suggestions: Optional[list[dict]]
    datetime: str

    @classmethod
    def from_dict(cls, data: dict):
        timestamp = data.get("time")
        return cls(
            title=data.get("title"),
            timestamp=timestamp,
            url=data.get("url") or data.get("link"),
            source=data.get("source"),
            suggestions=data.get("suggestions"),
            datetime=format_time(timestamp)
        )

class HistoricalNewsEvent(NewsEvent):
    previous_candles: Candles
    observation_candles: Candles
    performance_candles: Candles

    @classmethod
    def from_dict(cls, data: dict):
        base_event = NewsEvent.from_dict(data)
        return cls(
            title=base_event.title,
            timestamp=base_event.timestamp,
            url=base_event.url,
            source=base_event.source,
            suggestions=base_event.suggestions,
            datetime=base_event.datetime,
            previous_candles=data.get("previous_candles"),
            observation_candles=data.get("observation_candles"),
            performance_candles=data.get("performance_candles")
        )