import json
import logging

from logger import display_news, display_login_message
from sentiment_analysis import analyze_sentiment


def on_message(socket, message):
    if socket:
        logging.info(f"Raw WS Message ({socket.url}): {message}")

    try:
        news_event = json.loads(message)
        headline = news_event.get("title")

        if headline:
            display_news(headline, news_event)
            analyze_sentiment(news_event)
        else:
            display_login_message(news_event)

        # Uncomment to enable sentiment analysis
        # sentiment = analyze_sentiment(headline, content)
        # print(f"Sentiment: {sentiment}")


    except Exception as e:
        logging.error(f"[ERROR] Processing Error: {e}")