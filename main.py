import time

from backtest.back_test import load_historical_news, run_backtest
from config import IS_BACKTEST_MODE
from websocket.websocket_handler import init_connections
from websocket.message_handler import on_message
from logger import setup_logger

# Set up the logger only once in the main entry point
setup_logger()

# === Main Execution ===
if __name__ == "__main__":

    if IS_BACKTEST_MODE:
        news_data = load_historical_news()
        run_backtest(news_data, on_message)
    else:
        init_connections(on_message)
        print("🚀 Crypto AI News Trading Bot started. Listening to both WebSockets...")
        while True:
            time.sleep(10)