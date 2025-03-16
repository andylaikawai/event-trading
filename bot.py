import json
import time
import logging
from websocket_handler import init_connections
from trading import make_trade
from sentiment_analysis import analyze_sentiment

# === WebSocket Handling ===
def on_message(socket, message):
    try:
        logging.info(f"Raw WS Message ({socket.url}): {message}")

        news_event = json.loads(message)
        print(f"\n Raw message from {socket.url}: {news_event}")
        headline = news_event.get("title")
        content = news_event.get("body")

        # Extract and display timestamp
        timestamp_ms = news_event.get("time")
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp_ms / 1000))
        print(f"\n🌳 News @ {timestamp}: {headline}")
        print(f"🌳 Content @ {content}")

        # Uncomment to enable sentiment analysis
        # sentiment = analyze_sentiment(headline, content)
        # print(f"Sentiment: {sentiment}")

        # Extract trading symbols from suggestions if available
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

    except Exception as e:
        print(f"Processing Error: {e}")

# === Main Execution ===
if __name__ == "__main__":
    init_connections(on_message)

    print("🚀 Crypto AI News Trading Bot started. Listening to both WebSockets...")
    while True:
        time.sleep(10)