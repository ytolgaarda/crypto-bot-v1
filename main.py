import time
from configuration.config_manager import ConfigManager
from core.strategy import should_sell, should_buy
from core.trader import get_current_price, sell_order, buy_order, calculate_current_profit

cfg = ConfigManager("configuration/config.ini")
model = cfg.load_model()


def main():
    print("Bot başlangıç mevcut pozisyon:", model.position)

    while True:
        price = get_current_price(model.symbol)

        current_profit = calculate_current_profit(model, price)

        print(f"Güncel Fiyat : {price} USD | Satın Alınan Fiyat: {model.buy_price} | Güncel Kar: {current_profit} | Güncel Pozisyon: {model.position} ")

        # Alım
        if model.position in ["NONE", "SOLD"] and should_buy(price):
            print("Al Sinyali  (TEST)")
            result = buy_order(model.symbol, model.budget)
            print("✅ Alındı:", result)
            buy_price = price  # price * (1 + FEE_PERCENTAGE)  # Ücreti ekle
            qty = float(result["fills"][0]["qty"])
            model.position = "BOUGHT"
            model.buy_price = price
            model.holding_amount = qty
            model.cost = buy_price * qty  # Toplam maliyet
            # kalıcı olarak yaz
            cfg.set("position", model.position)
            cfg.set("buy_price", model.buy_price)
            cfg.set("holding_amount", model.holding_amount)
            cfg.set("cost", model.cost)

        # Satış
        elif model.position == "BOUGHT" and should_sell(price):
            print("Sat Sinyali (TEST)")
            result = sell_order(model.symbol, model.holding_amount, current_profit)
            print("✅ Satıldı:", result)
            model.position = "SOLD"
            cfg.set("position", model.position)
            cfg.set("buy_price", model.buy_price)
            cfg.set("holding_amount", 0.0)
            cfg.set("cost", 0.0)
            cfg.set("max_profit", 0.0)

        time.sleep(model.interval)


if __name__ == "__main__":
    main()
