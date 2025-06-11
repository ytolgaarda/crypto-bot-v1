from binance.spot import Spot
from configuration.key import API_KEY, API_SECRET


class BinanceClient:
    def __init__(self):
        # Binance Spot client'ını başlatır ve authenticate olur
        self.client = Spot(api_key=API_KEY, api_secret=API_SECRET)
        print("Binance client initialized and authenticated.")


# Dışarıdan erişmek için
client = BinanceClient()
