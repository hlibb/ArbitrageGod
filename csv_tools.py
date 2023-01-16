import csv
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates


def create_file():
    with open("project_data.csv", "w+", newline='') as file:
        writer = csv.writer(file)
        fieldnames = ['time', 'binance_price', 'huobi_price', 'kucoin_price']
        writer.writerow(fieldnames)


create_file()


def write_prices_down(time, binance_price, huobi_price, kucoin_price):
    with open("project_data.csv", "a", newline='') as file:
        writer = csv.writer(file)
        data = [str(time), str(binance_price), str(huobi_price), str(kucoin_price)]
        writer.writerow(data)


def create_graph():
    with open("project_data.csv", "r") as file:
        data = pd.read_csv(file)
        data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S')
        fig = plt.Figure()
        ax = fig.add_subplot(111)
        ax.plot(data['time'], data['binance_price'], label='binance_price')
        ax.plot(data['time'], data['huobi_price'], label='huobi_price')
        ax.plot(data['time'], data['kucoin_price'], label='kucoin_price')
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        ax.set_title('Price comparison')
        ax.legend()
        xfmt = mdates.DateFormatter('%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.gcf().autofmt_xdate()
        return fig
