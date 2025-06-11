from configuration.config_manager import ConfigManager

# ConfigManager’ı başlatıp ve modeli yükler
cfg = ConfigManager("configuration/config.ini")
model = cfg.load_model()


def should_sell(current_price: float) -> bool:
    fee = model.fee_percentage
    bp = model.buy_price
    mp = model.max_profit
    bpv = model.base_profit
    inc = model.profit_increment
    amt = model.holding_amount

    # Net satış fiyatı (işlem ücreti düşülmüş)
    net_sell_price = current_price * (1 - fee)

    # Gerçek kar (USD) = (net satış fiyatı - alış fiyatı) * miktar
    current_profit = (net_sell_price - bp) * amt

    # Eğer kar yeni maksimumun üzerine çıktıysa güncelle ve satma
    if current_profit > mp:
        model.max_profit = current_profit
        cfg.set("max_profit", current_profit)
        return False

    # Base kar eşiğini geçmiş ve profit_increment kadar düşmüşse sat
    if current_profit >= bpv and current_profit < model.max_profit - inc:
        return True

    return False


def should_buy(current_price: float) -> bool:
    # Eğer zaten alma pozisyonundada isek tekrar alma
    if model.position == "BOUGHT":
        return False
    # Bot yeni başladıysa veya pozisyon "NONE" ise direkt al
    if model.position == "NONE":
        print("Bot ilk kez çalışıyor, alım yapılacak.")
        return True
    # Eğer daha önce satıldıysa ve fiyat tekrar eski alış fiyatına geldiyse al
    if model.position == "SOLD" and current_price <= model.buy_price:
        print(f"Fiyat eski alım seviyesine ({model.buy_price}) düştü. Alım yapılabilir.")
        return True

    return False
