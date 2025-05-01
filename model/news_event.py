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
            url=data.get("url") or data.get("link"),
            suggestions=data.get("suggestions"),
            message=data.get("message"), # for login ws message only
            user=data.get("user"), # for login ws message only
            datetime = format_time(timestamp)
        )