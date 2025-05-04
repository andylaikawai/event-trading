import time

from backtest.back_test import run_backtest
from config import IS_BACKTEST_MODE, MAX_HOLDING_PERIOD, MAX_OBSERVATION_PERIOD, LOOK_BACK_PERIOD, TAKE_PROFIT, \
    STOP_LOSS
from logger import setup_logger
from model.trade_params import TradeParams
from websocket.websocket import init_connections
from websocket.websocket_message_handler import on_message

# Set up the logger only once in the main entry point
setup_logger()

# === Main Execution ===
# TODO use interfaces to support backtest and live trading dynamically
if __name__ == "__main__":
    trade_params = TradeParams(
        max_holding_period=MAX_HOLDING_PERIOD,
        max_observation_period=MAX_OBSERVATION_PERIOD,
        look_back_period=LOOK_BACK_PERIOD,
        take_profit=TAKE_PROFIT,
        stop_loss=STOP_LOSS
    )

    if IS_BACKTEST_MODE:
        run_backtest(trade_params)
    else:
        init_connections(on_message)
        print("🚀 Crypto AI News Trading Bot started. Listening to both WebSockets...")
        while True:
            time.sleep(10)
