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
from datetime import datetime
from pytz import timezone   
from WebscrapeStockData_Threaded import AssignWorkers, GithubUpdate 

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


# Pull live stock prices and append to dataframe
def dataframe_prices(dataframe):
    if dataframe.size >= 0:
        liveprice = AW.pull_live_price()
        if liveprice != None:
            df.loc[len(df)] = liveprice
        return df
    else:
        print('No dataframe passed to dataframe_prices')


# Eastern time required to determine open trading times
def stockmarket_openhours():
    # Get time now
    USA_East = timezone('US/Eastern')
    weekday = datetime.now(USA_East).weekday()
    hour = datetime.now(USA_East).hour
    
    # Simple logic to stop collecting data during market close
    if 4 <= weekday <= 6:
        if weekday == 4 and hour <= 17:
            return True
        elif weekday == 6 and hour >= 18:
            return True
        else:
            return False
    else:
        return True

          
# Main code with governing parameters
if __name__ == '__main__':
    # Required Parameters
    trigger = False     # trigger to stop collecting data on market close
    tickercolumn = 0    # which column are tickers in
    ticker_size = 150   # number of tickers used from Wiki URL
    threads = 10        # number of threads pulling ticker data
    pull_step = 60      # time (seconds) between price pull
    rows = 60           # number of rows before csv is pushed to Github (1 hour)
    
    # Minute by Minute filename
    m_by_m = 'minute_by_minute.csv'
    
    # Get tickers from Wiki URL
    webURL = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    filename = 'sp500tickers.pickle'
    tickers = save_FTSE250_tickers(0, webURL, filename)
    
    # Start webscraping threads
    AW = AssignWorkers()
    AW.assignworkers(tickerlist=tickers, tickerNo=ticker_size, workerNo=threads)
    
    # Initiate and start Github thread (required for financial data collection 
    # during github upload)
    GH = GithubUpdate();  GH.start()
    
    try:
        while stockmarket_openhours()==True or trigger==False:
            if stockmarket_openhours()==True:
                # Make empty dataframe to append to
                df = pd.DataFrame(columns = ['Date Time'] + tickers[:ticker_size])
                
                # Append price list to dataframe
                for i in range(0,rows):
                    df = dataframe_prices(dataframe = df)
                    time.sleep(pull_step)
        
                if not os.path.exists(m_by_m):
                    df.to_csv(m_by_m)
                    print(df)
                    print('\nCreated file for minute by minute data\n{} rows added'.format(len(df)-1))
                    GH.upload_github() 
                else:
                    # Append dataframe to csv file
                    df.to_csv(m_by_m, mode='a', header=False)
                    print(df)
                    print('\nAppended {} with more data\n{} rows added'.format(m_by_m, len(df)-1))
                    GH.upload_github()
                
                # trigger state changed to stop data collection on market close
                trigger = True
            else:
                print('\nMarkets are closed...\n')
                time.sleep(pull_step)
    except:
        print('Error Thrown in Main Script')
    
    # Stop threads when exiting while loop
    AW.stop_all()
    
    # Alert user that collecting has finished
    print('''
            ###############################\n
            No more data will be collected.\n
            ###############################''')  