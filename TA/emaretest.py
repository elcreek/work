import pandas as pd
import numpy as np

import datetime as dt
from binance.client import Client
# import asyncio


#import os
import telebot

client = Client()




import config
API_KEY = config.API_KEY

bot = telebot.TeleBot(API_KEY)





def get_historical_ohlc_data(symbol,days=35,interval='1h'):

    df=pd.DataFrame(client.get_historical_klines(symbol=symbol,start_str=f"{days} days ago UTC",interval=interval))

    df.columns=['open_time','open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol','is_best_match']
    df['open_date_time']=[dt.datetime.fromtimestamp(x/1000) for x in df.open_time]
    # df['symbol']=symbol
    df=df[['open_date_time','open', 'high', 'low', 'close', 'volume']]
    df.set_index('open_date_time', inplace=True)


    return df[:-1]


    


def clc(df):

    # df['ema50'] = pd.to_numeric(df["close"].rolling(50).mean())
    # df['ema200'] = pd.to_numeric(df["close"].rolling(200).mean())

    df['sma200'] = pd.to_numeric(df["close"].rolling(200).mean())
    # df['ema200'] = pd.to_numeric(df['Close'].ewm(span=200,min_periods=0,adjust=False,ignore_na=False).mean())
    df['low'] = pd.to_numeric(df['low'])
    df['close'] = pd.to_numeric(df['close'])



    # df['que'] = np.where((df['rsi'] < (df['ema_rsi']+df['ema_rsi']*0.03)) & (df['rsi'] > (df['ema_rsi']-df['ema_rsi']*0.03)), 1, 0)
    df['que'] = np.where((df['close'] <= (df['sma200']+df['sma200']*0.01)) & (df['low'] >= df['sma200']), 1, 0)

    # if df.index[-1].strftime('%d-%m-%Y') == pd.to_datetime("today").strftime('%d-%m-%Y'):
        

    if (df['que'].iloc[-1] == 1) or (df['que'].iloc[-2] == 1) :
        candy.append(f"{symbol}, {df.index[-1]}")





timeframes = ["1h"]

# 'VTHOBTC', 'BSVUSDT', 'BSVBTC', 'CKBBTC', 'SCBTC'
# pairs= ['AR/USDT', 'SYS/USDT', 'BSV/USDT', 'CKB/USDT', 'CTXC/USDT', 'DOGE/USDT', 'ETC/USDT', 'FIL/USDT', 'FIRO/USDT', 'LTC/USDT', 'KMD/USDT', 'RVN/USDT', 'SC/USDT', 'XLM/USDT', 'XMR/USDT', 'XRP/USDT', 'ZEC/USDT', 'ZEN/USDT', 'DGB/USDT', 'DASH/USDT', 'BCH/USDT', 'RNDR/USDT', 'VET/USDT', 'VTHO/USDT', 'KDA/USDT', 'NKN/USDT', 'AR/BTC', 'SYS/BTC', 'CTXC/BTC', 'DOGE/BTC', 'ETC/BTC', 'FIL/BTC', 'FIRO/BTC', 'LTC/BTC', 'KMD/BTC', 'RVN/BTC', 'SC/BTC', 'XLM/BTC', 'XMR/BTC', 'XRP/BTC', 'ZEC/BTC', 'ZEN/BTC', 'DGB/BTC', 'DASH/BTC', 'BCH/BTC', 'RNDR/BTC', 'VET/BTC', 'KDA/BTC', 'NKN/BTC']

pairs= ['ARUSDT', 'SYSUSDT', 'CKBUSDT', 'CTXCUSDT', 'DOGEUSDT', 'ETCUSDT', 'FILUSDT', 'FIROUSDT', 'LTCUSDT', 'KMDUSDT', 'RVNUSDT', 'SCUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'ZECUSDT', 'ZENUSDT', 'DGBUSDT', 'DASHUSDT', 'BCHUSDT', 'RNDRUSDT', 'VETUSDT', 'VTHOUSDT', 'KDAUSDT', 'NKNUSDT', 'ARBTC', 'SYSBTC', 'CTXCBTC', 'DOGEBTC', 'ETCBTC', 'FILBTC', 'FIROBTC', 'LTCBTC', 'KMDBTC', 'RVNBTC', 'XLMBTC', 'XMRBTC', 'XRPBTC', 'ZECBTC', 'ZENBTC', 'DGBBTC', 'DASHBTC', 'BCHBTC', 'RNDRBTC', 'VETBTC', 'KDABTC', 'NKNBTC']

# pairs=['BNBUSDT']

candy =[]


for timeframe in timeframes:

    for symbol in pairs:

        df= get_historical_ohlc_data(symbol, interval=timeframe)
            
        clc(df)
        

# asyncio.run(main())

print(candy)
