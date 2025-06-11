import configparser
import os
from model.config_model import ConfigModel


class ConfigManager:
    def __init__(self, path="config.ini"):
        self.path = path
        self.config = configparser.ConfigParser()
        if not os.path.exists(self.path):
            self._create_default()
        self.config.read(self.path)

    def _create_default(self):
        self.config["bot"] = {
            "position": "NONE",
            "buy_price": "0.0",
            "holding_amount": "0.0",
            "cost": "0.0",
            "max_profit": "0.0",
            "profit_increment": "0.1",
            "base_profit": "0.5",
            "budget": "50.0"
        }
        with open(self.path, "w") as f:
            self.config.write(f)

    def get(self, key, cast_type=str):
        val = self.config["bot"].get(key)
        if val is None:
            return None
        if cast_type is float:
            return float(val)
        if cast_type is int:
            return int(val)
        return val

    def set(self, key, value):
        self.config["bot"][key] = str(value)
        with open(self.path, "w") as f:
            self.config.write(f)

    def load_model(self) -> ConfigModel:
        b = self.get("base_profit", float)
        pi = self.get("profit_increment", float)
        mp = self.get("max_profit", float)
        ha = self.get("holding_amount", float)
        bp = self.get("buy_price", float)
        c = self.get("cost", float)
        pos = self.get("position", str)
        bud = self.get("budget", float)
        sym = self.get("symbol", str)
        interval = self.get("interval", int)
        fee = self.get("fee_percentage", float)

        return ConfigModel(
            position=pos,
            buy_price=bp,
            holding_amount=ha,
            cost=c,
            max_profit=mp,
            profit_increment=pi,
            base_profit=b,
            budget=bud,
            symbol=sym,
            interval=interval,
            fee_percentage=fee
        )

