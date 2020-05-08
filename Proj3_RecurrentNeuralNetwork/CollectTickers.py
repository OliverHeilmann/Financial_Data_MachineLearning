"""
Created on Tue Apr 14 15:54:50 2020

@author: OliverHeilmann
"""
import validators
import requests, pdb
import bs4 as bs
import pandas as pd
import pickle
import string
from yahoo_fin import stock_info as si
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

'''
use:
    %matplotlib qt        --> as po-pup
    %matplotlib inline    --> in shell
'''

# This script collects the necessary
class Market_Index_TickerList:    
    def __init__(self, s_filename=None, t_filename=None, yahooURL=None,
                 tickerURL=None, save=False, add_companies=None):
        self.s_filename = s_filename
        self.t_filename = t_filename
        self.yahooURL = yahooURL
        self.tickerURL = tickerURL   
        self.save = save
        self.add_companies = add_companies
       

    # Collect the Stock Exchange Suffixes from Yahoo Offical Website
    def yahoo_ticker_suffix(self):
        if self.s_filename[-7:] == '.pickle' and validators.url(self.yahooURL) == True:
            resp = requests.get(self.yahooURL)
            soup = bs.BeautifulSoup(resp.text, 'html.parser') # or lxml
            table = soup.find('table')
        
            # Get headers for dataframe
            headers = [ele.text.strip() for ele in table.find_all('th')]
            data = [[ele for ele in headers if ele]]
        
            # Get bulk data for dataframe. We skip first 'tr' because these are the 
            # headers which were collected in the above two lines of code.
            for row in table.findAll('tr')[1:]:
                cols = [ele.text.strip() for ele in row.find_all('td')]
                data.append([ele for ele in cols if ele])
                
            # Compile into dataframe using pandas
            df = pd.DataFrame(data)
            
             # Save dataframe to a pickle file
            if self.save:
                with open(self.s_filename, "wb") as f:
                    pickle.dump(df, f)
            return df
        else:
            print('Check input arguments in yahoo_ticker_suffix()')
            return None


    # Ensure ticker returns results and only pass succsesses
    def check_tickers(self, tickers):
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


    # Webscrape tickers from Wikipedia URL. This function should scan through 
    # all tables in a page so no need to define it specifically (unless mulitple
    # ticker tables are present).
    def scrape_tickers(self, suffix=''):
        if validators.url(self.tickerURL) == True:
            resp = requests.get(self.tickerURL)
            soup = bs.BeautifulSoup(resp.text, 'lxml')
            
            # Look through Wiki tables for ticker column header
            for table in soup.findAll('table', {'class': 'wikitable sortable'}):
                # Get headers for dataframe
                headers = [ele.text.strip() for ele in table.find_all('th')]
                data = [ele for ele in headers if ele]
                
                # Find column number of 'ticker' header
                for el in data:
                    if 'ticker' in el.lower() or 'symbol' in el.lower():
                        ticker_head_num = data.index(el)
                        
                        # Scan table for rows, extract tickers and append to list
                        tickers = []
                        for row in table.findAll('tr')[1:]:
                            ticker = row.findAll('td')[ticker_head_num]
                            ticker = ticker.text.replace('\n', '').upper()
                            ticker = ticker.translate(str.maketrans('','', string.punctuation))
                            ticker = ticker + suffix
                            tickers.append(ticker.strip())
                        
                        # Add any additional companies
                        if self.add_companies != None:
                            for company in self.add_companies:
                                if company not in tickers:
                                    tickers.append(company)
                        
                        # Call function to check if tickers return prices
                        # BELOW FUNCTION REDUNDANT WITH NEW UPDATES
                        #tickers = self.check_tickers(tickers)

                        # Save tickers to a pickle file
                        if self.save:
                            with open(self.t_filename, "wb") as f:
                                pickle.dump(tickers, f)

                        print(tickers)
                        return tickers
        
        # Either Wikipedia link is incorrect or Ticker Table not found in link
        print('''
        NO TICKERS FOUND!
            Check input arguments in scrape_tickers(). Either Wikipedia 
            link is incorrect or ticker table is not found in provided 
            link. If this link is not from Wikipedia tickers may not be 
            exported.
             ''')
        return None
        

    # Request market information from user
    def choose_market(self):
        # Collect suffix data from yahoo
        df = self.yahoo_ticker_suffix()
        
        # Prompt user to select one Market/Index from global list.
        print('Choose a market or index from the following list:')
        i = 1
        for row in df[1][1:]:
            print('   {}) {}'.format(i, row))
            i += 1
            
        # Request answer from user and convert to integer
        ans = int(input('INPUT ROW NUMBER HERE (e.g. "1"): '))

        # Extract relevant suffix from dataframe based on user response. If no
        # suffix exists then Yahoo does not require any additional information. 
        # This is the case for American Stock Exchanges.
        suffix = df[2][ans]
        if suffix.lower() == 'n/a':
            suffix = ''
        
        # Pass suffix to webscraped ticker list
        tickers = self.scrape_tickers(suffix)
        return tickers