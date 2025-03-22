import logging
import time

def setup_logger(log_file='logs/ws_messages.log'):
    # Logger Configuration
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        level=logging.INFO,
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
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp_ms / 1000))
    source = news_event.get("link") or news_event.get("url") or "-"

    print(f"\n🌳 Timestamp: {timestamp}")
    print(f"News: {headline}")
    print(f"Source: {source}")

    logging.info(f"{timestamp} - Headline: '{headline}' | Source: '{source}'")
