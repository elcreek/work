import ccxt
import os
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
# import sys
# import shutil
# from functools import partial
# from pathlib import Path


exchange = ccxt.binance()

exchange.load_markets()

symbols = exchange.symbols


t = 'USDT'
pairs = []
# global unwanted
unwanted = ["XNO","BTT","GYEN","UP/","DOWN/","USDS","USDT/","USDSB","SUSD",
"NCASH/ETH","DNT/ETH","BCN/ETH","UST","ETH/","BKRW","VAI","RUB",
"NGN","DAI","BIDR","BEAR", "BULL", "PAX", "TUSD", "UMA", "USDC",
 "USDP", "BUSD/", "EUR", "GBP", "TRY", "AUD","BRL", "BVND"]

for s in symbols:
    if (t in s):
        pairs.append(s)

pairs=[n for n in pairs if all(m not in n for m in unwanted)]


_pairs = ["ATOM/USDT"]

# always put the list out of the loop or everthing will be wiped out each turn

timeframes = ["1h", "4h", "1d"]
# limit = 1003

# td =datetime.now().strftime('%Y-%m-%d_%H')

for timeframe in timeframes:

    for symbol in tqdm(pairs):

        m_symbol = symbol.replace("/","")
        outname = f"{m_symbol}_{timeframe}.csv"

        # outdir=f"{os.getcwd()}/data/{td}/{timeframe}"
        outdir=f"{os.getcwd()}/data/{timeframe}"
        # outdir=f"{os.getenv('HOME')}/data/{td}/{timeframe}"
        fullname = os.path.join(outdir, outname) 

        # remove old dir
        # if os.path.exists(outdir):
        #     shutil.rmtree(outdir)

        if not os.path.exists(outdir):
            os.makedirs(outdir)

        bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=1001)
        # must use bars[:-1] because arrgrelextrema will see the last candle wich have not closed yet
        data = pd.DataFrame(bars[:-1], columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        data['Time'] = pd.to_datetime(data['Time'], unit='ms')
        data.set_index('Time', inplace=True)
        if len(data) < 20:
            print("data less than 20 candles for ", symbol)
            continue

        data.to_csv(fullname) 
        # print('fetching new data', symbol)
    


  
            
