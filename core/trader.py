from core.binance_client import client
from datetime import datetime
from core.log_manager import LogManager

log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_manager = LogManager()

def get_current_price(symbol: str = "BTCUSDT") -> float:
    ticker = client.client.ticker_price(symbol)
    return float(ticker["price"])


def sell_order(symbol: str, quantity: float,current_profit: float):
    # İşlem yapılmadan önce loglama
    log_message = f"TEST SATIM EMİRİ -> Symbol: {symbol}, Quantity: {quantity} | Edilen Kar: {current_profit}// [{log_time}]"
    print(log_message)
    log_manager.write(log_message)

    return {
            "status": "FILLED",
            "side": "SELL",
            "symbol": symbol,
            "executedQty": str(quantity),
            "fills": [
                {
                    "price": str(get_current_price(symbol)),
                    "qty": str(quantity),
                    "commission": "0.00000001",
                    "commissionAsset": "BTC"
                }
            ]
    }


# Gerçek işlem
   # order = client.client.new_order(
   #     symbol=symbol,
   #     side="SELL",
   #     type="MARKET",
   #     quantity=quantity
   # )
   # return order


def buy_order(symbol: str, amount_usdt: float):
    price = get_current_price(symbol)
    quantity = round(amount_usdt / price, 6)
    # İşlem yapılmadan önce loglama
    log_message = f"TEST ALIM EMİRİ -> Symbol: {symbol}, Amount USDT: {amount_usdt}, Quantity: {quantity} // [{log_time}]"
    print(log_message)
    log_manager.write(log_message)

    return {
        "status": "FILLED",
        "side": "BUY",
        "symbol": symbol,
        "price": str(price),
        "executedQty": str(quantity),
        "fills": [
            {
                "price": str(price),
                "qty": str(quantity),
                "commission": "0.00000001",
                "commissionAsset": "BTC"
            }
        ]
    }
    # Gerçek işlem
    # order = client.client.new_order(
    #     symbol=symbol,
    #     side="BUY",
    #     type="MARKET",
    #     quantity=quantity
    # )
    # return order


def calculate_current_profit(model, current_price: float) -> float:
    if model.position != "BOUGHT":
        return 0.0
    fee = model.fee_percentage
    bp = model.buy_price
    amt = model.holding_amount

    # Net satış fiyatı (fee düşüldü)
    net_sell_price = current_price * (1 - fee)

    # Kar = (net satış fiyatı - alış fiyatı) * miktar
    profit = (net_sell_price - bp) * amt
    return profit

