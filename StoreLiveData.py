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
import requests, pdb
import string

# Webscrape from Wikipedia URLs (consider non real time)
def save_FTSE250_tickers(tickercolumn=0, website=None):
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
            with open("FTSE250.pickle", "wb") as f:
                pickle.dump(tickers, f)
            return tickers
        return None
    except:
        print('Likely not a Wikipedia URL...')


#class LivePrice(Thread, picklepath="FTSE250.pickle", quantity=100):
#    def pull_liveprice(picklepath="FTSE250.pickle", quantity=100):
#        with open(picklepath, "rb") as f:
#            tickers = pickle.load(f)
#        
#        # Get live price for tickers
        

print(save_FTSE250_tickers(1, 'https://en.wikipedia.org/wiki/FTSE_250_Index'))