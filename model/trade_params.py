from dataclasses import dataclass


@dataclass
class TradeParams:
    max_holding_period: int
    max_observation_period: int
    look_back_period: int
    take_profit: float = 0.0
    stop_loss: float =  0.0
