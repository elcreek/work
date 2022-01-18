from datetime import datetime
import os
from time import time
from typing import ClassVar
import yfinance as yf
import pandas as pd
from flask import Flask, render_template
# from patterns import patterns
import tqdm
from binance import Client

api_key = '0Tbt22Cx2LDoKFIKRdabh4BXmVOzJggkhvCJ9GvgyzYT1wqfpgTqilOIYJrqkc5l'
api_secret = 'ucOlFt3RB72gzAoxaHKFTNFTTIUDcayK8qMQFkvzqOuugtuqG4WqQbknmcFZvpfR'

client = Client(api_key, api_secret)

klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_1MINUTE, "1 Dec, 2021")
df = pd.DataFrame(klines)
df.to_csv("ETHBTC.csv")

# with open('datasets/tickers.csv') as f:
#         symbols = f.read().splitlines()
#         for symbol in symbols:
#             klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, "1 Jan, 2010")
#             df = pd.DataFrame(klines)
#             df.to_csv("datasets\daily\{}.csv".format(symbol))

# screener_parttime_larry

# def update_csv():
#     get last row unix time
#     convert it to datetime
#     use get historical kline 
#     append to old Csv


# if unix_time_today != last_row_unix_time:
#     call update_csv