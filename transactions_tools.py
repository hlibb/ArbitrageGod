import account_tools as at
import csv_tools as ct
import requests
import json
import datetime


def get_coin_price_on_binance(symbol):
    key = "https://api.binance.com/api/v3/ticker/price?symbol={}USDT".format(symbol)
    data = requests.get(key)
    data = data.json()
    return float(data['price'][:8])


def get_coin_price_on_huobi(symbol):
    url = 'https://api.huobi.pro/market/trade?symbol={}usdt'.format(symbol.lower())
    response = requests.request('GET', url)
    r = json.loads(response.text)
    return float(r['tick']['data'][0]['price'])


def get_coin_price_on_kucoin(symbol):
    url = 'https://api.kucoin.com'
    rex = requests.get(url + '/api/v1/market/orderbook/level1?symbol={}-USDT'.format(symbol),
                       data={'data': 'price'}).json()
    return float(rex['data']['price'])


def transaction_available(price_max, price_min):
    if price_max / price_min >= 1.00001:
        return True
    else:
        return False


def get_prices():  # price check
    b_price = get_coin_price_on_binance(at.coin_symbol)  # binance price
    h_price = get_coin_price_on_huobi(at.coin_symbol)  # huobi price
    k_price = get_coin_price_on_kucoin(at.coin_symbol)  # kucoin price
    return [b_price, h_price, k_price]  # [0 - Binance, 1 - Huobi, 2 - Kucoin]


def output_line_creation(selling_wallet_name, selling_sum_of_crypto, selling_sum_of_fiat, buying_wallet_name,
                         buying_sum_of_fiat, prices):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    ct.write_prices_down(current_time, prices[0], prices[1], prices[2])
    return f"|{current_time}| {selling_wallet_name.title()} " \
           f"SELL {selling_sum_of_crypto} ${at.coin_symbol}({selling_sum_of_fiat}$), " \
           f"{buying_wallet_name.title()} BUY {selling_sum_of_crypto} ${at.coin_symbol}({buying_sum_of_fiat}$)"


def update_session_income(selling_sum_of_fiat, buying_sum_of_fiat):
    at.session_income += (selling_sum_of_fiat - buying_sum_of_fiat)  # income during the transaction


def transaction_itself(index_selling_wallet, selling_sum_of_crypto, price_maxima, index_buying_wallet, price_minima):
    at.wallets[index_selling_wallet][1]['crypto'] -= selling_sum_of_crypto  # minus crypto from binance_wallet
    at.wallets[index_selling_wallet][1]['fiat'] += (
            selling_sum_of_crypto * price_maxima)  # plus fiat in binance_wallet
    at.wallets[index_buying_wallet][1]['crypto'] += selling_sum_of_crypto  # + crypto
    at.wallets[index_buying_wallet][1]['fiat'] -= (selling_sum_of_crypto * price_minima)  # - fiat


def transaction():
    prices = get_prices()
    price_minima = min(prices)
    price_maxima = max(prices)
    if transaction_available(price_maxima, price_minima):
        index_selling_wallet = prices.index(price_maxima)  # binance crypto costs more
        selling_wallet_name = at.wallets[index_selling_wallet][0]
        index_buying_wallet = prices.index(price_minima)  # huobi costs less
        buying_wallet_name = at.wallets[index_buying_wallet][0]
        selling_sum_of_crypto = at.wallets[index_selling_wallet][1]['crypto'] * 0.1  # binance wallet crypto
        buying_sum_of_fiat = price_minima * selling_sum_of_crypto
        selling_sum_of_fiat = selling_sum_of_crypto * prices[index_selling_wallet]
        transaction_itself(index_selling_wallet, selling_sum_of_crypto, price_maxima, index_buying_wallet, price_minima)
        update_session_income(selling_sum_of_fiat, buying_sum_of_fiat)
        result = output_line_creation(selling_wallet_name, selling_sum_of_crypto, selling_sum_of_fiat,
                                      buying_wallet_name, buying_sum_of_fiat, prices)
        at.history.append(result)
        return result
    else:
        return ""


def start_transactions():
    for i in range(60):  # set the number of transaction loops
        result = transaction()
        if result != "":
            print(result)
