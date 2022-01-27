import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# import yfinance as yf
from scipy.signal import argrelextrema
# from collections import deque
# from matplotlib.lines import Line2D
import pandas_ta as ta
import ccxt
from datetime import datetime, timedelta
# import plotly.graph_objects as go
# import inspect 
import os
import ccxt_data_fetch

# pd.set_option('display.max_rows', 50)

exchange = ccxt.binance()

exchange.load_markets()

symbols = exchange.symbols

def ccxt_data(symbol='ETH/USDT', timeframe ='1d', limit=111):

    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    # must use bars[:-1] because arrgrelextrema will see the last candle wich have not closed yet
    data = pd.DataFrame(bars[:-1], columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    data['Time'] = pd.to_datetime(data['Time'], unit='ms')
    data.set_index('Time', inplace=True)
    
    return data


def calc():
    data=ccxt_data()

    order=10
    global peaks_df
    global troughs_df

    if len(data) > 14:
    
        # data=ccxt_data()
        # calc indicator
        data['ta_rsi'] = ta.rsi(data['Close'], length = 14)

        # if (data['ta_rsi'].size > 14) and (data['Close'].size > 14) :
        # calc peaks and troughs of close price and the indicator(s)
        coin_peak = argrelextrema(data['Close'].values, np.greater, order=order)[0]
        # print(coin_peak)
        coin_peaks_df = data.iloc[coin_peak]['Close']
        # print(coin_peaks_df)

        ta_peak = argrelextrema(data['ta_rsi'].values, np.greater, order=order)[0]
        ta_peaks_df = data.iloc[ta_peak]['ta_rsi']
        # print(ta_peaks_df)

        coin_trough = argrelextrema(data['Close'].values, np.less, order=order)[0]
        coin_trough_df = data.iloc[coin_trough]['Close']

        ta_trough = argrelextrema(data['ta_rsi'].values, np.less, order=order)[0]
        ta_trough_df = data.iloc[ta_trough]['ta_rsi']

        peaks = [coin_peaks_df, ta_peaks_df]
        peaks_df = pd.concat(peaks, axis=1)
        peaks_df = peaks_df[(peaks_df.Close.notna()) & (peaks_df.ta_rsi.notna())]

        troughs = [coin_trough_df, ta_trough_df]
        troughs_df = pd.concat(troughs, axis=1)
        troughs_df = troughs_df[(troughs_df.Close.notna()) & (troughs_df.ta_rsi.notna())]

        if peaks_df.empty:
            # tof=False
            print('empty peaks')
            return False
        elif troughs_df.empty:
            print('empty troughs')
            return False
        else:
            return peaks_df, troughs_df, True

    else:
        # tof=False
        print('data length less than 14')
        return False


calc()

n=9
dates_of_peaks = []
if len(peaks_df) >= n:
    for i in range(5):
        if i == 0:
            diff = peaks_df.diff(1)
            sig = diff[~((diff > 0).all(1)) & ~((diff < 0).all(1))]
        #     dates_of_peaks.append(sig.index.values)
        #     continue
        # diff = peaks_df.diff(i)
        # sig = diff[~((diff > 0).all(1)) & ~((diff < 0).all(1))]
        # dates_of_peaks.append(sig.index.values)
else:
    for i in range(len(peaks_df)-1):
        if i == 0:
            diff = peaks_df.diff(1)
            sig = diff[~((diff > 0).all(1)) & ~((diff < 0).all(1))]
        #     dates_of_peaks.append(sig.index.values)
        #     continue
        # diff = peaks_df.diff(i)
        # sig = diff[~((diff > 0).all(1)) & ~((diff < 0).all(1))]
        # dates_of_peaks.append(sig.index.values)

# dates_of_peaks
