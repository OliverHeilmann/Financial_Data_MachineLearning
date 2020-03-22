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

1) stockmarket_openhours: should add public holidays and webscrape the trading
                          times rather than require a manual input.

'''
import bs4 as bs
import pickle
import requests
import pdb, time, os
import string
import pandas as pd
from datetime import datetime
from pytz import timezone 
from yahoo_fin import stock_info as si  
from WebscrapeStockData_Threaded import AssignWorkers, GithubUpdate 


# Ensure ticker returns results
def check_tickers(tickers):
    print('Checking Tickers')
    total_tickers = len(tickers)
    for ticker in tickers:
        # Provide user with loading information of % completion
        print('----> {} %'.format(round((tickers.index(ticker)+1)*100/len(tickers),1)))
        try:
            val = si.get_live_price(ticker)
            if val != float(val):
                print('\n\n{} has not been found\n\n'.format(ticker))
                tickers.remove(ticker)    
        except:
            print('\n\n{} has not been found\n\n'.format(ticker))
            tickers.remove(ticker)
    print('########### {}/{} passed ###########'.format(len(tickers),total_tickers))
    return tickers


# Webscrape from Wikipedia URLs (consider non real time)
def save_tickers(tickercolumn=0, website=None, filename=None, LSE=False):
    try:
        if website != None:
            resp = requests.get(website)
            soup = bs.BeautifulSoup(resp.text, 'lxml')
            table = soup.find('table', {'class': 'wikitable sortable'})
            tickers = []
            for row in table.findAll('tr')[1:]:
                ticker = row.findAll('td')[tickercolumn].text.replace('\n', '').upper()
                ticker = ticker.translate(str.maketrans('', '', string.punctuation))
                if LSE == True:
                    ticker = ticker + '.L'
                tickers.append(ticker)
            tickers = check_tickers(tickers[:ticker_size])  # check tickers
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
        # Append dataframe with new data
        if liveprice != [None]:
            df.loc[len(df)] = liveprice
        return df
    else:
        print('No dataframe passed to dataframe_prices')


# Small function to send T/F logic for Exchange Trading Times
def stockmarket_openhours(tmzone, m_open, m_close):
    # Get day of week
    weekday = datetime.now(tmzone).weekday()
    if m_open <= datetime.now(tmzone) <= m_close and weekday <= 4:
        return True
    return False

          
# Main code with governing parameters
if __name__ == '__main__':
    ############## MANUAL PARAMETERS REQUIRED TO BE SET BELOW ################
    tickercolumn = 1    # which column are tickers in
    ticker_size = 250   # number of tickers used from Wiki URL
    threads = 10        # number of threads pulling ticker data (1 per CPU core)
    pull_step = 60      # time (60 seconds) between price pull
    rows = 15           # number of rows before csv is pushed to Github (1 hour)
    zone = timezone('Europe/London')    # set the timezone of stock market
    LSE = True          # London Stock Exchange? If it is assign as 'True'. The
                        # reason for this is the tickers require '.L' at end of
                        # name to be detected in Yahoo Finance
    
    # Set Market Open/ Close times (must add the times in)
    now = datetime.now(zone)
    m_open = now.replace(hour=8, minute=0, second=0, microsecond=0)
    m_close = now.replace(hour=16, minute=30, second=0, microsecond=0)
    
    # Minute by Minute filename
    filename = 'minute_by_minute.csv'
    
    # Get tickers from Wiki URL
    #webURL = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    #filename = 'sp500tickers.pickle'
    webURL = 'https://en.wikipedia.org/wiki/FTSE_250_Index'
    picklename = 'FTSE250.pickle'
    
    ####################### END OF MANUAL PARAMETERS #########################
    
    # Collect list of tickers
    tickers = save_tickers(tickercolumn, webURL, picklename, LSE)     
    
    # Start webscraping threads
    AW = AssignWorkers()
    AW.assignworkers(tickerlist=tickers, tickerNo=ticker_size, workerNo=threads)
    
    # Initiate and start Github thread (required for financial data collection 
    # during github upload)
    GH = GithubUpdate(filepath=filename);  GH.start()
    #GH.upload_github()  # ensure Github and script are up to date
    time.sleep(5)
    
    #Main loop giving stock collection instructions
    try:
        while True:
            if stockmarket_openhours(zone, m_open, m_close)==True:
                # Make empty dataframe to append to
                df = pd.DataFrame(columns = ['Date Time'] + tickers[:ticker_size])
                
                # Append price list to dataframe if markets are open
                for i in range(0,rows):
                    # IF statement to check if markets are open
                    if datetime.now(zone) <= m_close:
                        df = dataframe_prices(dataframe = df)
                        print('Collecting stock prices every {} seconds...'.format(pull_step))
                        time.sleep(pull_step)
        
                if not os.path.exists(filename):
                    df.to_csv(filename)
                    print(df)
                    print('\n\nCreated filepath...\n{} rows added\n\n'.format(len(df)-1))
                    GH.upload_github() 
                else:
                    # Append dataframe to csv file
                    df.to_csv(filename, mode='a', header=False)
                    print(df)
                    print('\nAppended {}...\n{} rows added\b'.format(filename, len(df)))
                    GH.upload_github()
            else:
                print('Markets are closed...\n')
                time.sleep(pull_step)
    except:
        print('Exiting Main Loop...')
    
    # Stop threads when exiting while loop
    AW.stop_all()   # stop workers
    GH.stop()       # stop Github
    
    # Alert user that collecting has finished
    print('''
            ###############################\n
            No more data will be collected.\n
            ###############################''')  