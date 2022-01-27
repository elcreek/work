import ccxt
import os
import pandas as pd
from datetime import datetime, timedelta



exchange = ccxt.binance()

# exchange = ccxt.binance({
#     'enableRateLimit': True,
# })


# exchange.enableRateLimit = True 
exchange.load_markets()

symbols = exchange.symbols


# ticker = 'BTC-USDT'
# timeframe ='4h'
# use bars[:-1] to avoid false signal espeacially in current candle
# because ccxt gives the ongoing candle before they close
# do bars[:-3] to get less trades; but better quality
def ccxt_data(symbol='ETH/USDT', timeframe ='4h', limit=111):
    global data
    # global fullname

    m_symbol = symbol.replace("/","_")
    outname = m_symbol+'_'+timeframe+'_'+f'{limit}'+'.csv'
    outdir=os.getcwd()+f'/data/{timeframe}'
    fullname = os.path.join(outdir, outname)    

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    if not (os.path.exists(fullname)):

        bars = exchange.fetch_ohlcv(symbol, timeframe, limit)
        # must use bars[:-1] because arrgrelextrema will see the last candle wich have not closed yet
        data = pd.DataFrame(bars[:], columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        data['Time'] = pd.to_datetime(data['Time'], unit='ms')
        data.set_index('Time', inplace=True)

        data.to_csv(fullname) 
        print('fetching new data', symbol)
    
    else:
        tem_data = pd.read_csv(fullname, index_col='Time')
        # last_candle_time=tem_data['Time'].max()
        last_candle_time_plus=pd.to_datetime(tem_data.index[-1]) + pd.Timedelta(12, unit="h")
        if (last_candle_time_plus) >= pd.to_datetime(datetime.now()) :
            data = tem_data
        else:
            bars = exchange.fetch_ohlcv(symbol, timeframe, limit)
            data = pd.DataFrame(bars[:], columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            data['Time'] = pd.to_datetime(data['Time'], unit='ms')
            data.set_index('Time', inplace=True)

            data.to_csv(fullname)
            print('updating data ',symbol)
            
   
    return data