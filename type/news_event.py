from typing import NamedTuple, List, Optional

from utils.util import format_time


class NewsEvent(NamedTuple):
    title: Optional[str]
    time: int
    link: Optional[str]
    url: Optional[str]
    suggestions: Optional[List[dict]]
    message: Optional[str]
    user: Optional[dict]
    datetime: str

    @staticmethod
    def from_dict(data: dict):
        timestamp = data.get("time", 0)
        return NewsEvent(
            title=data.get("title"),
            time=timestamp,
            link=data.get("link"),
            url=data.get("url"),
            suggestions=data.get("suggestions"),
            message=data.get("message"),
            user=data.get("user"),
            datetime = format_time(timestamp)
        )