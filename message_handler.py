# message_handler.py

import json
import logging
import time

from trading import make_trade
from sentiment_analysis import analyze_sentiment

def on_message(socket, message):
    try:
        logging.info(f"Raw WS Message ({socket.url}): {message}")

        news_event = json.loads(message)
        headline = news_event.get("title")

        # Display news information
        if headline:
            display_news(headline, news_event)
            process_suggestions(news_event)
        else:
            username = news_event.get("user", {}).get("username", "-")
            login_message = news_event.get("message") or f"Logged in as {username} successfully"
            display_message(login_message)

        # Uncomment to enable sentiment analysis
        # sentiment = analyze_sentiment(headline, content)
        # print(f"Sentiment: {sentiment}")


    except Exception as e:
        print(f"Processing Error: {e}")

def display_message(message):
    print(f"{message}\n")
    logging.info(f"{message}")

def display_news(headline, news_event):
    timestamp_ms = news_event.get("time", 0)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp_ms / 1000))
    content = news_event.get("body", "-")
    source = news_event.get("link") or news_event.get("url") or "-"

    """Display the news details."""
    print(f"\n🌳 Timestamp: {timestamp}")
    print(f"News: {headline}")
    print(f"Source: {source}")
    print(f"Content:")
    print(f"""```\n{content}\n```""")

    logging.info(f"{timestamp} - Headline: '{headline}' | Source: '{source}'")


def process_suggestions(news_event):
    """Process trading suggestions from the news event."""
    suggestions = news_event.get("suggestions", [])
    if suggestions:
        for suggestion in suggestions:
            coin = suggestion.get("coin")
            if coin:
                print(f"Relevant coin identified: {coin}")
                # Uncomment to enable trade execution
                # make_trade(market_symbol, sentiment)
                return
    else:
        print("No suitable KuCoin trading symbol found in suggestions.")