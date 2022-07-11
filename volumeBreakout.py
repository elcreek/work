'''//@version=3
study(title="Volume Based S/R", shorttitle="VSR", precision=0, overlay=true)

length = input(20, minval=1)
change = volume/volume[1] - 1  # the previous bar: volume[1]
stdev = stdev(change, length)
difference = change / stdev[1]
Treshold = input(5)
zero = 0
signal = abs(difference)

leveluphi = valuewhen(signal > Treshold,high[1],0)
leveluplo = valuewhen(signal > Treshold,low[1],0)

//plot(UpperTreshold, color=black)
p1 = plot(leveluphi,style=circles,color=blue)
p2 = plot(leveluplo,style=circles,color=blue)
fill(p1,p2,color=green,transp=90)
//plot(abs(sigma), color = palette, style=columns, title="Volume", transp=65)'''

import pandas as pd
import numpy as np

import datetime as dt
from binance.client import Client
import asyncio
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




timeframes = ["1h"]

pairs= ['ARUSDT', 'SYSUSDT', 'CKBUSDT', 'CTXCUSDT', 'DOGEUSDT', 'ETCUSDT', 'FILUSDT', 'FIROUSDT', 'LTCUSDT', 'KMDUSDT', 'RVNUSDT', 'SCUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'ZECUSDT', 'ZENUSDT', 'DGBUSDT', 'DASHUSDT', 'BCHUSDT', 'RNDRUSDT', 'VETUSDT', 'VTHOUSDT', 'KDAUSDT', 'NKNUSDT', 'ARBTC', 'SYSBTC', 'CTXCBTC', 'DOGEBTC', 'ETCBTC', 'FILBTC', 'FIROBTC', 'LTCBTC', 'KMDBTC', 'RVNBTC', 'XLMBTC', 'XMRBTC', 'XRPBTC', 'ZECBTC', 'ZENBTC', 'DGBBTC', 'DASHBTC', 'BCHBTC', 'RNDRBTC', 'VETBTC', 'KDABTC', 'NKNBTC']
# pairs=['BCHUSDT']
candy =[]

for timeframe in timeframes:

    for symbol in pairs:

        df=get_historical_ohlc_data(symbol, interval=timeframe)
            
        # clc(df, symbol)
        df['prevvol'] = df['volume'].shift()
        df= df.dropna()

        ###########################

        df['prevvol'] = pd.to_numeric(df['prevvol'])
        df['volume'] = pd.to_numeric(df['volume'])

        df['change'] = (df['volume'] / df['prevvol']) - 1

        ##################################

        df['stdev'] = df['change'].rolling(20).std()

        ####################

        df['prevstd'] = df['stdev'].shift()

        df['prevstd'] = pd.to_numeric(df['prevstd'])
        df['change'] = pd.to_numeric(df['change'])

        df['difference'] = df['change'] / df['prevstd']

        Treshold = 5
        zero = 0
        df['signal'] = df['difference'].abs()
        df= df.dropna()

        df['leveluphi'] = np.where(df['signal'] > Treshold,1,0)
        # df['leveluplo'] = np.where(df['signal'] > Treshold,2,0)

        # if (df['leveluphi'].values == 1) or (df['leveluplo'].values == 2) :
        #     candy.append(f"{symbol}")

        print(symbol, df[df['signal'] > Treshold])

# print(df[:])
# print(candy)

# asyncio.run(main())



    


