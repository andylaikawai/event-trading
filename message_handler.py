# message_handler.py

import json
import logging
from logger import display_news, display_login_message
from trading import make_trade
from sentiment_analysis import analyze_sentiment

def on_message(socket, message):
    if socket:
        logging.info(f"Raw WS Message ({socket.url}): {message}")

    try:
        news_event = json.loads(message)
        headline = news_event.get("title")

        if headline:
            display_news(headline, news_event)
            process_suggestions(news_event)
        else:
            display_login_message(news_event)

        # Uncomment to enable sentiment analysis
        # sentiment = analyze_sentiment(headline, content)
        # print(f"Sentiment: {sentiment}")


    except Exception as e:
        print(f"Processing Error: {e}")

def process_suggestions(news_event):
    suggestions = news_event.get("suggestions")
    if suggestions:
        for suggestion in suggestions:
            coin = suggestion.get("coin")
            if coin:
                print(f"Relevant coin identified: {coin}")
                # Uncomment to enable trade execution
                # make_trade(market_symbol, sentiment)
                return
    else:
        print("No suitable trading symbol found in suggestions.")