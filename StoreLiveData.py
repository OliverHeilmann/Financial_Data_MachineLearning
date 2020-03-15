#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 22:57:22 2020

@author: OliverHeilmann

My next task is to webscrape minute by minute data for FTSE 500 companies.
7 days of data should be sufficient here as this is 604,800 total sample which
is likely far more than is required.

Reqs:
    -upload regularly to github. This means regular pushes (and pulls to reduce
     load on the computer)
    -crash prevention/ preventative measures
    -real time public holiday and non-trading hours web scraping
    -create new github account for Jetson and allow admin rights so that it 
     does not interfere with my projects
    -If companies fall out of FTSE 500 they should still be tracked. Any new 
     companies entering will be added to the tracked list as well- pickle this
     list.

Other:
    -web traffic bot
"""


'''
Notes: 
    -Ok, webscrape FTSE 250 and use top 150. If they fall below the 150 mark 
    stil track them. If they fall outside 250 then whoops!The correlation 
    between these companies may drop so this should be considered later on. We
    will tackle this later on.

'''
import bs4 as bs
import pickle
import requests
import pdb, time, os
import string
import pandas as pd
from WebscrapeStockData_Threaded import AssignWorkers

# Webscrape from Wikipedia URLs (consider non real time)
def save_FTSE250_tickers(tickercolumn=0, website=None, filename=None):
    try:
        if website != None:
            resp = requests.get(website)
            soup = bs.BeautifulSoup(resp.text, 'lxml')
            table = soup.find('table', {'class': 'wikitable sortable'})
            tickers = []
            for row in table.findAll('tr')[1:]:
                ticker = row.findAll('td')[tickercolumn].text.replace('\n', '').upper()
                ticker = ticker.translate(str.maketrans('', '', string.punctuation)) #del punctuation
                tickers.append(ticker)
            with open(filename, "wb") as f:
                pickle.dump(tickers, f)
            return tickers
        return None
    except:
        print('Likely not a Wikipedia URL...')

def dataframe_prices(dataframe = None):
    if dataframe != None:
        liveprice = AW.pull_live_price()
        if liveprice != None:
            df.loc[len(df)] = liveprice
        return df
    else:
        print('Missing parameters in dataframe_prices')
            

if __name__ == '__main__':
    # Required Parameters
    tickercolumn = 0
    ticker_size = 10
    
    # Get tickers from Wiki URL
    webURL = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    filename = 'sb500tickers.pickle'
    tickers = save_FTSE250_tickers(0, webURL, filename)
    
    # Make empty dataframe to append to
    df = pd.DataFrame(columns = ['Date Time'] + tickers[:ticker_size])
    
    # Start webscraping threads
    AW = AssignWorkers()
    AW.assignworkers(tickerlist=tickers, tickerNo = ticker_size, workerNo = 5)
    
    # Append price list to dataframe
    dataframe = dataframe_prices(dataframe = df)
    
    for i in range(0,20):
        liveprice = AW.pull_live_price()
        if liveprice != None:
            df.loc[len(df)] = liveprice
            print(df)
        time.sleep(1)
    AW.stop_all()
    


    
    
    
    
    
    
    
    
    
    
    