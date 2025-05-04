import optuna

from backtest.back_test import run_backtest
from model.trade_params import TradeParams

"""
Optuna uses Bayesian Optimization to efficiently search the parameter space. 
It does not randomly test parameters but instead builds a probabilistic model of the objective function and uses it to decide which parameters to evaluate next. 

Here's how it works:


1. Initialization:
Optuna starts with a few random trials to explore the parameter space.

2. Modeling:
It builds a surrogate model (e.g., a Gaussian Process or Tree-structured Parzen Estimator) to approximate the relationship between parameters and the objective function.

3. Acquisition Function:
Optuna uses an acquisition function (e.g., Expected Improvement) to balance exploration (trying new areas) and exploitation (refining known good areas).
The acquisition function suggests the next set of parameters to evaluate.

4. Iterative Improvement:
After each trial, Optuna updates the surrogate model with the new results and repeats the process.

This approach allows Optuna to focus on promising regions of the parameter space, making it more efficient than random or grid search.
"""


def objective(trial):
    max_holding_period = trial.suggest_int("max_holding_period", 30, 59)
    max_observation_period = trial.suggest_int("max_observation_period", 3, 3)
    look_back_period = trial.suggest_int("look_back_period", 3, 10)
    take_profit = trial.suggest_float("take_profit", 0.05, 0.3)
    stop_loss = trial.suggest_float("stop_loss", -0.05, -0.005)

    trade_params = TradeParams(
        max_holding_period=max_holding_period,
        max_observation_period=max_observation_period,
        look_back_period=look_back_period,
        take_profit=take_profit,
        stop_loss=stop_loss
    )
    return run_backtest(trade_params)


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=100)

print("Best parameters:", study.best_params)
print("Best ROI:", study.best_value)
