import logging
import time

from config import LOG_LEVEL
from utils.util import format_time


def setup_logger(log_file='logs/ws_messages.log'):
    logging.basicConfig(
        filename=log_file,
        filemode='w',
        level=LOG_LEVEL,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def display_login_message(news_event):
    message = news_event.get("message")
    username = news_event.get("user", {}).get("username")
    login_message = message or f"Logged in as {username} successfully\n"

    print(f"{login_message}")
    logging.info(f"{login_message}")


def display_news(headline, news_event):
    timestamp_ms = news_event.get("time", 0)
    timestamp = format_time(timestamp_ms)
    source = news_event.get("link") or news_event.get("url") or "-"

    print(f"\n🌳 Timestamp: {timestamp}")
    print(f"Headline: {headline}")
    print(f"Source: {source}")

    logging.debug(f"{timestamp} - Headline: '{headline}' | Source: '{source}'")
