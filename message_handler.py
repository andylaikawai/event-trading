# message_handler.py

import json
import logging
import time
from trading import make_trade
from sentiment_analysis import analyze_sentiment

def on_message(socket, message):
    try:
        # Log the raw message as a JSON field
        logging.info("New message received", extra={"json_message": message})

        news_event = json.loads(message)
        headline = news_event.get("title", "N/A")
        content = news_event.get("body", "N/A")
        timestamp_ms = news_event.get("time", 0)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp_ms / 1000))

        # Display news information
        display_news(timestamp, headline, content)

        # Uncomment to enable sentiment analysis
        # sentiment = analyze_sentiment(headline, content)
        # print(f"Sentiment: {sentiment}")

        process_suggestions(news_event)

    except Exception as e:
        print(f"Processing Error: {e}")

def display_news(timestamp, headline, content):
    """Display the news details."""
    print(f"\n🌳 News @ {timestamp}: {headline}")
    print(f"🌳 Content @ {content}")

def process_suggestions(news_event):
    """Process trading suggestions from the news event."""
    suggestions = news_event.get("suggestions", [])
    if suggestions:
        for suggestion in suggestions:
            symbols = suggestion.get("symbols", [])
            for sym in symbols:
                if sym["exchange"] == "kucoin":
                    market_symbol = sym["symbol"]
                    print(f"Trading symbol identified: {market_symbol}")
                    # Uncomment to enable trade execution
                    # make_trade(market_symbol, sentiment)
                    return  # trade only first matched symbol
    else:
        print("No suitable KuCoin trading symbol found in suggestions.")