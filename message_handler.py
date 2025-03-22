import json
import logging

from logger import display_news, display_login_message
from sentiment_analysis import analyze_sentiment
from type.news_event import NewsEvent


def on_message(socket, message):
    if socket:
        logging.info(f"Raw WS Message ({socket.url}): {message}")

    try:
        news_event = NewsEvent.from_dict(json.loads(message))

        if news_event.title:
            display_news(news_event)
            analyze_sentiment(news_event)
        else:
            display_login_message(news_event)

    except Exception as e:
        logging.error(f"[ERROR] Processing Error: {e}")