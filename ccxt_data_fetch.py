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
    # i use globl for data variable even thogh the function returns data variable
    # because jupyter cells are ceperated from each other

    m_symbol = symbol.replace("/","_")
    outname = m_symbol+'_'+timeframe+'_'+f'{limit}'+'.csv'
    outdir=os.getcwd()+f'/data/{timeframe}'
    fullname = os.path.join(outdir, outname)    

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    if not (os.path.exists(fullname)):

        bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        # must use bars[:-1] because arrgrelextrema will see the last candle wich have not closed yet
        data = pd.DataFrame(bars[:], columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        data['Time'] = pd.to_datetime(data['Time'], unit='ms')
        data.set_index('Time', inplace=True)

        data.to_csv(fullname) 
        print('fetching new data', symbol)
    
    else:
        tem_data = pd.read_csv(fullname, index_col='Time')
        # last_candle_time=tem_data['Time'].max()
        # print(type(tem_data.index[-1]))
        # c =pd.to_datetime(tem_data.index[-1])
        # d =  c- datetime.now()
        # print(c, d)
        if tem_data.empty:
            os.remove(fullname)

        if pd.to_datetime(tem_data.index[-1]) < (pd.to_datetime(datetime.now()) - pd.Timedelta(8, unit="h")):
            os.remove(fullname)
        
        elif pd.to_datetime(tem_data.index[-1]) + pd.Timedelta(4, unit="h") > pd.to_datetime(datetime.now()):
            data = tem_data
        # ll=pd.to_datetime(datetime.now()) - pd.Timedelta(4, unit="h")

        # if ll in tem_data.index:
        #     if ll == tem_data.index[-1]:
        #         data = tem_data
        else:
            bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            data = pd.DataFrame(bars[:], columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            data['Time'] = pd.to_datetime(data['Time'], unit='ms')
            data.set_index('Time', inplace=True)

            data.to_csv(fullname)
            print('updating data ',symbol)
            
   
    return data

# ccxt_data()