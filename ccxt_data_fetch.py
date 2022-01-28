import ccxt
import os
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
from functools import partial
from pathlib import Path


exchange = ccxt.binance()

exchange.load_markets()

symbols = exchange.symbols


t = 'USDT'
pairs = []
# global unwanted
unwanted = ["GYEN","UP/","DOWN/","USDS","USDT/","USDSB","SUSD",
"NCASH/ETH","DNT/ETH","BCN/ETH","UST","ETH/","BKRW","VAI","RUB",
"NGN","DAI","BIDR","BEAR", "BULL", "PAX", "TUSD", "UMA", "USDC",
 "USDP", "BUSD/", "EUR", "GBP", "TRY", "AUD","BRL", "BVND"]

for s in symbols:
    if (t in s):
        pairs.append(s)

pairs=[n for n in pairs if all(m not in n for m in unwanted)]


_pairs = ["ETH/USDT","ATOM/USDT"]

# always put the list out of the loop or everthing will be wiped out each turn
order=5
timeframe = '1d'
limit = 111
rows = []
td =datetime.now().strftime('%Y-%m-%d_%H')
# global tof
for symbol in tqdm(pairs):

    m_symbol = symbol.replace("/","_")
    outname = m_symbol+'_'+timeframe+'_'+f'{limit}'+'.csv'

    outdir=f"{os.getcwd()}/data/{td}/{timeframe}"
    # outdir=f"{os.getenv('HOME')}/data/{td}/{timeframe}"
    fullname = os.path.join(outdir, outname) 
   

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if not (os.path.exists(fullname)):
        bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        # must use bars[:-1] because arrgrelextrema will see the last candle wich have not closed yet
        data = pd.DataFrame(bars[:], columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        data['Time'] = pd.to_datetime(data['Time'], unit='ms')
        data.set_index('Time', inplace=True)

        data.to_csv(fullname) 
        # print('fetching new data', symbol)
    

 
  
            
