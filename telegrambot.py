#import os
import pandas as pd
import numpy as np
import telebot
import talib
import pandas_ta as ta
import datetime as dt
from binance.client import Client
from scipy.signal import argrelextrema

client = Client()


API_KEY = '5336229182:AAFZG8_9m3RaNOlZVZ0oqmPz_xEdk80mXUQ'
bot = telebot.TeleBot(API_KEY)


def calc(data):
    # data=ccxt_data() # using it will reset all the params to default parms
    # symbol='ETH/USDT'

    # global order
    global peaks_df
    global troughs_df    

    if len(data) > 14:
    

        data['ta_rsi'] = ta.rsi(data['Close'], length = 14)

        coin_peak = argrelextrema(data['Close'].values, np.greater, order=5)[0]
        coin_peaks_df = data.iloc[coin_peak]['Close']

        #high instead of close
        # coin_peak = argrelextrema(data['High'].values, np.greater, order=order)[0]
        # coin_peaks_df = data.iloc[coin_peak]['High']
  

        ta_peak = argrelextrema(data['ta_rsi'].values, np.greater, order=5)[0]
        ta_peaks_df = data.iloc[ta_peak]['ta_rsi']
 

        coin_trough = argrelextrema(data['Close'].values, np.less, order=5)[0]
        coin_trough_df = data.iloc[coin_trough]['Close']

        # low instaed of close
        # coin_trough = argrelextrema(data['Low'].values, np.less, order=order)[0]
        # coin_trough_df = data.iloc[coin_trough]['Low']

        ta_trough = argrelextrema(data['ta_rsi'].values, np.less, order=5)[0]
        ta_trough_df = data.iloc[ta_trough]['ta_rsi']

        peaks = [coin_peaks_df, ta_peaks_df]
        peaks_df = pd.concat(peaks, axis=1)
        peaks_df = peaks_df[(peaks_df.Close.notna()) & (peaks_df.ta_rsi.notna())]

        #high instead of close
        # peaks_df = peaks_df[(peaks_df.High.notna()) & (peaks_df.ta_rsi.notna())]


        troughs = [coin_trough_df, ta_trough_df]
        troughs_df = pd.concat(troughs, axis=1)
        troughs_df = troughs_df[(troughs_df.Close.notna()) & (troughs_df.ta_rsi.notna())]

        #low instead of close
        # troughs_df = troughs_df[(troughs_df.Low.notna()) & (troughs_df.ta_rsi.notna())]

        if peaks_df.empty:
            # tof=False
            # print('empty peaks', symbol)
            return False

        elif troughs_df.empty:
            # print('empty troughs', symbol)
            return False
        
        else:
            return peaks_df, troughs_df, True

    else:
        # tof=False
        ## print('data length less than 14', symbol)
        return False


def signal_dates(data, n=9):
    global sell
    global buy
    sell = []
    buy = []

    # global dates_of_peaks
    dates_of_peaks = []
    
    dates_of_troughs = []

    if calc(data):

        for i in range(1,n):

            diff = peaks_df.diff(i)
            # diff.dropna(inplace=True) # do not use it
            sig = diff[~((diff > 0).all(1)) & ~((diff < 0).all(1))]
            dates_of_peaks.append(sig.index.values)

    
            diff = troughs_df.diff(i)
            # diff.dropna(inplace=True) # do not use it
            sig = diff[~((diff > 0).all(1)) & ~((diff < 0).all(1))]
            dates_of_troughs.append(sig.index.values)

        for list in dates_of_peaks:
            for i in list:
                if str(i) not in sell:
                    # np.datetime to str
                    # maybe pd.to_datetime(i) works better
                    sell.append(str(i))

        for list in dates_of_troughs:
            for i in list:
                if str(i) not in buy:
                    buy.append(str(i))
                    

        sell.sort()
        buy.sort()

        # print(dates_of_peaks)
        # problem : buy ans sell should be list of datetime***********************

        # sell=pd.to_datetime(sell)
        # buy=pd.to_datetime(buy)


        if not buy or not sell:
            print('empty buy or sell')
            return False
        else:
            return sell, buy, True

    
            
    else:
        # tof=False
        # print(' calc() is false ', symbol)
        return False


def get_historical_ohlc_data(symbol, interval='1h'):
  # print(symbol)
  
  df = pd.DataFrame(
      client.get_historical_klines(symbol=symbol, start_str="33 days ago UTC", interval=interval))

  df.columns = [
      'open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'close_time',
      'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol',
      'is_best_match'
  ]
  df['Time'] = [
      dt.datetime.utcfromtimestamp(x / 1000) for x in df.open_time
  ]
  df = df[['Time', 'Open', 'High', 'Low', 'Close', 'Volume']]
  df.Close = df.Close.astype(float)
  df.set_index('Time', inplace=True)
#   print(df)
  return df[:-1]



pairs= ['FLUXUSDT', 'DREPUSDT', 'HOTUSDT' ,'ARUSDT', 'SYSUSDT', 'CKBUSDT',\
        'CTXCUSDT', 'DOGEUSDT', 'ETCUSDT','FILUSDT','FIROUSDT', 'LTCUSDT',\
        'KMDUSDT', 'RVNUSDT', 'SCUSDT', 'XLMUSDT',\
        'XMRUSDT', 'XRPUSDT', 'ZECUSDT', 'ZENUSDT', 'DGBUSDT', 'DASHUSDT',\
        'BCHUSDT', 'RNDRUSDT', 'KDAUSDT', 'NKNUSDT']


# n=9
# order=5

# # def go(n=9, order=5):
# for symbol in pairs:
#     data = get_historical_ohlc_data(symbol, interval='4h')
#     calc(data)
#     signal_dates(n)

#     # print(f'buy : \n{buy[-1]} \n{buy[-2]} \n{buy[-3]} \nsell : \n{sell[-1]}')
#     if signal_dates(n):
#         if (buy[-1] < sell[-1]) and (dt.datetime.now().strftime("%Y-%m-%d") <= sell[-1]):
#             print(symbol)
#             print(f'sell : {sell[-1]}')
#         elif (buy[-1] > sell[-1]) and (dt.datetime.now().strftime("%Y-%m-%d") <= buy[-1]):
#             print(symbol)
#             print(f'buy : {buy[-1]}')
#         else:
#             continue


# go()

#######


@bot.message_handler(commands=['1'])
def quarters(message):
    try:
        bot.send_message(chat_id=message.chat.id, text="running")

        n=9
        order=5

        # def go(n=9, order=5):
        for symbol in pairs:
            data = get_historical_ohlc_data(symbol, interval='1h')
            calc(data)
            signal_dates(data, n)

            # print(f'buy : \n{buy[-1]} \n{buy[-2]} \n{buy[-3]} \nsell : \n{sell[-1]}')
            if signal_dates(data, n):
                if (buy[-1] < sell[-1]) and (dt.datetime.now().strftime("%Y-%m-%d") <= sell[-1]):
                    # print(symbol)
                    # print(f'sell : {sell[-1]}')
                    bot.send_message(chat_id=message.chat.id, text=f'sell : {symbol} {sell[-1]}')
                elif (buy[-1] > sell[-1]) and (dt.datetime.now().strftime("%Y-%m-%d") <= buy[-1]):
                    # print(symbol)
                    # print(f'buy : {buy[-1]}')
                    bot.send_message(chat_id=message.chat.id, text=f'buy : {symbol} {buy[-1]}')

                else:
                    continue

    except:
        bot.send_message(chat_id=message.chat.id, text="err")
        pass


#########################


@bot.message_handler(commands=['2'])
def quarters(message):
    try:
        bot.send_message(chat_id=message.chat.id, text="running")

        n=9
        order=5

        # def go(n=9, order=5):
        for symbol in pairs:
            data = get_historical_ohlc_data(symbol, interval='2h')
            calc(data)
            signal_dates(data, n)

            # print(f'buy : \n{buy[-1]} \n{buy[-2]} \n{buy[-3]} \nsell : \n{sell[-1]}')
            if signal_dates(data, n):
                if (buy[-1] < sell[-1]) and (dt.datetime.now().strftime("%Y-%m-%d") <= sell[-1]):
                    # print(symbol)
                    # print(f'sell : {sell[-1]}')
                    bot.send_message(chat_id=message.chat.id, text=f'sell : {symbol} {sell[-1]}')
                elif (buy[-1] > sell[-1]) and (dt.datetime.now().strftime("%Y-%m-%d") <= buy[-1]):
                    # print(symbol)
                    # print(f'buy : {buy[-1]}')
                    bot.send_message(chat_id=message.chat.id, text=f'buy : {symbol} {buy[-1]}')

                else:
                    continue

    except:
        bot.send_message(chat_id=message.chat.id, text="err")
        pass


# ##########
@bot.message_handler(commands=['4'])
def quarters(message):
    try:
        bot.send_message(chat_id=message.chat.id, text="running")

        n=9
        order=5

        # def go(n=9, order=5):
        for symbol in pairs:
            data = get_historical_ohlc_data(symbol, interval='4h')
            calc(data)
            signal_dates(data, n)

            # print(f'buy : \n{buy[-1]} \n{buy[-2]} \n{buy[-3]} \nsell : \n{sell[-1]}')
            if signal_dates(data, n):
                if (buy[-1] < sell[-1]) and (dt.datetime.now().strftime("%Y-%m-%d") <= sell[-1]):
                    # print(symbol)
                    # print(f'sell : {sell[-1]}')
                    bot.send_message(chat_id=message.chat.id, text=f'sell : {symbol} {sell[-1]}')
                elif (buy[-1] > sell[-1]) and (dt.datetime.now().strftime("%Y-%m-%d") <= buy[-1]):
                    # print(symbol)
                    # print(f'buy : {buy[-1]}')
                    bot.send_message(chat_id=message.chat.id, text=f'buy : {symbol} {buy[-1]}')

                else:
                    continue

    except:
        bot.send_message(chat_id=message.chat.id, text="err")
        pass


######################

bot.polling()
