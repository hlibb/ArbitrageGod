# wallet default settings
coins = ("BTC", "ETH", "DOGE", "SOL", "MATIC")
binance_wallet = {'fiat': 0, 'crypto': 0}
huobi_wallet = {'fiat': 0, 'crypto': 0}
kucoin_wallet = {'fiat': 0, 'crypto': 0}
wallets = [["binance", binance_wallet], ["huobi", huobi_wallet], ["kucoin", kucoin_wallet]]
coin_symbol = ""
history = []
session_income = 0


def collect_input(b_entry_f, b_entry_c, h_entry_f, h_entry_c, k_entry_f, k_entry_c):
    binance_fiat_balance = b_entry_f.get()
    binance_coin_balance = b_entry_c.get()
    huobi_fiat_balance = h_entry_f.get()
    huobi_coin_balance = h_entry_c.get()
    kucoin_fiat_balance = k_entry_f.get()
    kucoin_coin_balance = k_entry_c.get()

    binance_wallet['fiat'] = int(binance_fiat_balance)
    binance_wallet['crypto'] = int(binance_coin_balance)
    huobi_wallet['fiat'] = int(huobi_fiat_balance)
    huobi_wallet['crypto'] = int(huobi_coin_balance)
    kucoin_wallet['fiat'] = int(kucoin_fiat_balance)
    kucoin_wallet['crypto'] = int(kucoin_coin_balance)
