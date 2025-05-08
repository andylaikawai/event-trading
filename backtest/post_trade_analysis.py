import logging
from typing import Union

from config import STARTING_CAPITAL
from model.candles import Candles
from model.news_event import HistoricalNewsEvent
from utils.util import round_to_2dp


def post_trade_analysis(news_event: HistoricalNewsEvent) -> None:
    # TODO identify missed opportunities
    market_moved = _detect_price_movement(news_event.performance_candles)

    if market_moved:
        source = news_event.url or "-"
        logging.debug(f"{news_event.title}")
        logging.debug(f"[ANALYSIS] Market moved by {market_moved:.2f}% at {news_event.datetime} for news: {source}")


def get_roi_percent(current_capital: float) -> float:
    if current_capital == 0:
        return 0.0
    roi_percent = (current_capital - STARTING_CAPITAL) / STARTING_CAPITAL * 100
    return round_to_2dp(roi_percent)[0]


def get_evaluation_result(trades: list[dict], current_capital: float):
    total_pnl = sum(trade['pnl'] for trade in trades if trade['pnl'] is not None)
    return_on_investment = get_roi_percent(current_capital)
    win_ratio = _get_win_ratio(trades)
    return total_pnl, return_on_investment, win_ratio


def log_performance(trades: list[dict], current_capital: float):
    [total_pnl, return_on_investment, win_ratio] = get_evaluation_result(trades, current_capital)
    [formatted_total_pnl, formatted_roi, formatted_win_ratio] = round_to_2dp(total_pnl, return_on_investment, win_ratio)

    logging.info(f"[TRADE] Total trades made: {len(trades)}")
    logging.info(f"[TRADE] Total PnL: {formatted_total_pnl}")
    logging.info(f"[TRADE] Win Ratio: {formatted_win_ratio}%")
    logging.info(f"[TRADE] ROI: {formatted_roi}%")


def log_top_trades(trades: list[dict]):
    if not trades:
        logging.info("[EVALUATION] No trades to evaluate.")
        return

    sorted_trades = sorted(trades, key=lambda trade: trade['pnl'], reverse=True)

    # Get top 10 gainers and losers
    top_gainers = sorted_trades[:10]
    top_losers = sorted_trades[-10:]

    logging.info("[EVALUATION] Top 10 Gainers:")
    for trade in top_gainers:
        logging.info(trade)

    logging.info("[EVALUATION] Top 10 Losers:")
    for trade in reversed(top_losers):  # Reverse to show the largest losses first
        logging.info(trade)


def _get_win_ratio(trades: list[dict]) -> float:
    if not trades:
        return 0.0
    winning_trades = sum(1 for trade in trades if trade['pnl'] > 0)
    return winning_trades / len(trades) * 100


def _detect_price_movement(candles: Candles) -> Union[float, None]:
    """Detect if the market price moved by more than 2%."""
    if candles is None or len(candles) < 2:
        return None

    initial_price = candles[0].close
    final_price = candles[-1].close

    price_change = (final_price - initial_price) / initial_price

    abs_price_change = abs(price_change)
    if abs_price_change > 0.02:
        return price_change * 100

    return None
