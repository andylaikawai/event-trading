import itertools
from backtest.back_test import run_backtest
from model.trade_params import TradeParams

def grid_search():
    # Define parameter ranges
    max_holding_period_range = range(30, 60)
    max_observation_period_range = [3]
    look_back_period_range = range(3, 11)
    take_profit_range = [x / 100 for x in range(5, 31)]  # 0.05 to 0.3
    stop_loss_range = [-x / 100 for x in range(5, 0, -1)]  # -0.05 to -0.005

    # Generate all combinations of parameters
    param_combinations = itertools.product(
        max_holding_period_range,
        max_observation_period_range,
        look_back_period_range,
        take_profit_range,
        stop_loss_range
    )

    best_params = None
    best_roi = float('-inf')

    # Evaluate each combination
    for combination in param_combinations:
        max_holding_period, max_observation_period, look_back_period, take_profit, stop_loss = combination

        trade_params = TradeParams(
            max_holding_period=max_holding_period,
            max_observation_period=max_observation_period,
            look_back_period=look_back_period,
            take_profit=take_profit,
            stop_loss=stop_loss
        )

        roi = run_backtest(trade_params)

        print(f"Trial: {trade_params}, ROI: {roi}")
        print(f"Best Trial: {best_params}, ROI: {best_roi}")

        if roi > best_roi:
            best_roi = roi
            best_params = trade_params

    print("Best parameters:", best_params)
    print("Best ROI:", best_roi)

# Run the grid search
grid_search()