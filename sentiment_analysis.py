from trading.sentiment_processor import execute_trade_based_on_signals


def _process_suggestions(news_event):
    suggestions = news_event.get("suggestions")
    if suggestions:
        for suggestion in suggestions:
            coin = suggestion.get("coin")
            if coin:
                print(f"Relevant coin identified: {coin}")
                return coin
    else:
        print("No suitable trading symbol found in suggestions.")
        return None

def analyze_sentiment(news_event):
    symbol = _process_suggestions(news_event)
    timestamp = news_event.get("time")

    if symbol == "BTC":
        execute_trade_based_on_signals(symbol, timestamp)
    return


# def analyze_sentiment(news_event):
#
#     prompt = f"""
#     Determine sentiment (Positive, Negative, Neutral) for the following crypto news. Respond with ONE word only.
#
#     Headline: {headline}
#     Content: {content}
#     Sentiment:
#     """
#     # To implement: Call to OpenAI or another sentiment analysis API
#     return "Neutral"  # Placeholder return value