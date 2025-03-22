import logging
import time

from config import LOG_LEVEL
from type.news_event import NewsEvent
from utils.util import format_time


def setup_logger():
    log_file = f'logs/ws_messages_{time.strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        filename=log_file,
        filemode='w',
        level=LOG_LEVEL,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # FileHandler to write logs to a file
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logging.getLogger().addHandler(file_handler)

    # Add a StreamHandler to flush logs immediately
    handler = logging.StreamHandler()
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logging.getLogger().addHandler(handler)


def display_login_message(news_event: NewsEvent):
    message = news_event.message
    username = news_event.user.get("username") if news_event.user else None
    login_message = message or f"Logged in as {username} successfully\n"

    print(f"{login_message}")
    logging.info(f"{login_message}")

def display_news(news_event: NewsEvent):
    timestamp_ms = news_event.time
    timestamp = format_time(timestamp_ms)
    source = news_event.link or news_event.url or "-"

    logging.debug(f"{timestamp} - Headline: '{news_event.title}' | Source: '{source}'")
