import time

from backtest.back_test import run_backtest
from backtest.historical_news_event_handler import on_historical_news_event
from config import IS_BACKTEST_MODE
from data.scripts.data_preprocessor import get_preprocessed_news
from logger import setup_logger
from websocket.websocket import init_connections
from websocket.websocket_message_handler import on_message

# Set up the logger only once in the main entry point
setup_logger()

# === Main Execution ===
if __name__ == "__main__":

    # TODO use interfaces to support backtest and live trading dynamically

    if IS_BACKTEST_MODE:
        historical_news_event = get_preprocessed_news()
        run_backtest(historical_news_event, on_historical_news_event)
    else:
        init_connections(on_message)
        print("🚀 Crypto AI News Trading Bot started. Listening to both WebSockets...")
        while True:
            time.sleep(10)
