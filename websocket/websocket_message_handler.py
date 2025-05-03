import json
import logging

from logger import display_news, display_login_message
from model.news_event import NewsEvent


def on_message(socket, message):
    if socket:
        logging.info(f"Raw WS Message ({socket.url}): {message}")

    try:
        raw_news_event = json.loads(message)
        news_event = NewsEvent.from_dict(raw_news_event)

        if news_event.title:
            display_news(news_event)
            # TODO
            # analyze_sentiment(news_event)
        else:
            display_login_message(raw_news_event.get('user'), raw_news_event.get('message'))

    except Exception as e:
        logging.error(f"[ERROR] Processing Error: {e}")