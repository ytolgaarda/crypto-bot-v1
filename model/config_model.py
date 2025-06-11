from dataclasses import dataclass


@dataclass
class ConfigModel:
    position: str
    buy_price: float
    holding_amount: float
    cost: float
    max_profit: float
    profit_increment: float
    base_profit: float
    budget: float
    symbol: str
    interval: int
    fee_percentage: float

    def to_dict(self):
        return {
            "position": self.position,
            "buy_price": self.buy_price,
            "holding_amount": self.holding_amount,
            "cost": self.cost,
            "max_profit": self.max_profit,
            "profit_increment": self.profit_increment,
            "base_profit": self.base_profit,
            "budget": self.budget,
            "symbol": self.symbol,
            "interval": self.interval,
            "fee_percentage": self.fee_percentage
        }
