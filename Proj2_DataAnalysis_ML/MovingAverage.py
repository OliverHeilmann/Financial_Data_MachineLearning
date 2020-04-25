#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:51:39 2020

@author: OliverHeilmann
"""
import pdb
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
from matplotlib.pylab import rcParams
style.use('ggplot')
rcParams['figure.figsize'] = 12,8

'''
use:
    %matplotlib qt        --> as po-pup
    %matplotlib inline    --> in shell
'''

def tradevol_adjclose(TVAJfile=None, Pfile=None,showday=100, days=5, TpBt=10):
    clean_df = pd.read_csv(TVAJfile, parse_dates=True, index_col=0)
    price_df = pd.read_csv(Pfile, parse_dates=True, index_col=0)

    # Find top/bottom performing companies in the past X days
    topX = clean_df[clean_df.iloc[-days:].mean().nlargest(TpBt).index]
    botX = clean_df[clean_df.iloc[-days:].mean().nsmallest(TpBt).index]
    alltop = pd.concat([topX, botX], axis=1)
    print('The best performing companies are as follows:\n',topX)
    print('The worst performing companies are as follows:\n',botX)
    
    # Get Top/Bottom Ticker Price data
    cols = [i.replace('_V/AP','') for i in alltop.columns]
    price_df = price_df[cols][-showday:]
    
    # Only care about last 'showday' days
    topX = topX[-showday:]
    botX = botX[-showday:]
    alltop = alltop[-showday:]
    
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('''
                 Top/Bottom {} Performing Companies
                 [TV/AC]% Averaged Over {} Days
                 '''.format(TpBt, days), size=20)

    ax1 = plt.subplot2grid((16,1), (1,0), rowspan=7, colspan=1)
    ax2 = plt.subplot2grid((16,1), (9,0), rowspan=3, colspan=1, sharex=ax1)
    ax3 = plt.subplot2grid((16,1), (13,0), rowspan=3, colspan=1, sharex=ax1)
    ax1.xaxis_date()
     
    ax1.set(ylabel='Top {} and Bottom {}\nStock Price [GBS]'.format(TpBt,TpBt))
    ax2.set(ylabel='Top {}\n[TV/AC]%'.format(TpBt))
    ax3.set(xlabel='Date', ylabel='Bottom {}\n[TV/AC]%'.format(TpBt))

    # Assigning labels to data
    lab1=[i for i in price_df.columns]
    lab2=[i for i in price_df.columns[:TpBt]]
    lab3=[i for i in price_df.columns[TpBt:]]
    
#    NUM_COLORS = 20
#    cm = plt.get_cmap('gist_rainbow')
#    ax1.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
#    ax2.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
#    ax3.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    
    # NOTE COLORS ONLY GO UP TO 7 AND THEN REPEAT (i.e. LEGEND IS NOT USEFUL)
    color_cycle = plt.rcParams['axes.prop_cycle']()
    for i in lab1:
        ax1.plot(topX.index, price_df[i], label=i)
        if i in lab2:
            ax2.plot(topX.index, topX[i+'_V/AP'], label=i, **next(color_cycle))
        if i in lab3:
            ax3.plot(botX.index, botX[i+'_V/AP'], label=i, **next(color_cycle))
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right')
    plt.show()
    

def candlestickplot(ticker):
    filename = 'stock_dfs/{}.csv'.format(ticker)
    df = pd.read_csv(filename, parse_dates=True, index_col=0)
    #df = df.iloc[-2000:]
    
    df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
    df['20ma'] = df['Adj Close'].rolling(window=20, min_periods=0).mean()
    
    df_ohlc = df['Adj Close'].resample('5D').ohlc()
    df_volume = df['Volume'].resample('5D').sum()
    
    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('{} Stock Date'.format(ticker), size=25)
    
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((10,1), (6,0), rowspan=4, colspan=1, sharex=ax1)
    ax1.xaxis_date()
    
    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
    
    ax1.set(ylabel='Stock Price')
    ax2.set(xlabel='Date', ylabel='Trade Volume')
    
    #ax1.plot(df.index, df['Adj Close'])
    ax1.plot(df.index, df['100ma'])
    ax1.plot(df.index, df['20ma'])
    ax2.bar(df.index, df['Volume'])

    plt.show()
    
if __name__ == '__main__':
    f1 = 'TV_AC_Dataframe.csv'
    f2 = 'PricesDF.csv'
    ticker='BAB.L'
    #candlestickplot(ticker)
    tradevol_adjclose(TVAJfile=f1, Pfile= f2, showday=200, days=3, TpBt=4)