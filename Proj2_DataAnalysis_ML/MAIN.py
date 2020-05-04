"""
Created on Wed Apr  8 20:03:38 2020
@author: OliverHeilmann

This script webscrapes wikipedia for a list of tickers (which you must provide
the link for). Depending on which country list you intend to use (e.g. London
Stock Exchange or S&P500), Yahoo finance uses a suffix notation for the companies.

After collecting your ticker list, the appropraite suffixes are webscraped from
the official Yahoo Finance page and then appended to your ticker list.

A folder is created to collect all the financial data for the companies you 
have selected. A csv file is created for each company in your ticker list. A 
final compiled csv file contains all the close prices for your ticker list- the
user defines a time frame to collect data from (e.g. June till August).

Finally, all close price is plotted on a graph. Additionally, a Correlation 
Table is generated.
"""
import pandas as pd
import pickle
import os, pdb
import numpy as np; np.random.seed(1)
import datetime as dt
from datetime import datetime
from pandas_datareader import data as pdr
from pandas.plotting import register_matplotlib_converters
from CollectTickers import Market_Index_TickerList
from InteractivePlotter import visualize_corr_data, time_series_plot
from VolPrice_ML import tickerML
from MovingAverage import tradevol_adjclose, candlestickplot
register_matplotlib_converters()

'''
use:
    %matplotlib qt        --> as po-pup
    %matplotlib inline    --> in shell
'''

# Getting ticker data from Yahoo
def get_data_from_yahoo(reload=False, ticker_funct=None, picklepath=None, startdate=[2000,1,1]):
    if reload:
        tickers = ticker_funct.choose_market()
    else:
        with open(picklepath, "rb") as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start = dt.datetime(startdate[0],startdate[1],startdate[2])
    end = dt.datetime.now()
    rmlist = []
    for ticker in tickers:
        try:
            print(ticker)
            df = abs(pdr.get_data_yahoo(ticker, start, end))
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
                print('Created file for {} data\n'.format(ticker))
            else:
                prev = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
                prev.set_index("Date", inplace=True)
                if len(prev) != len(df):
                    df.to_csv('stock_dfs/{}.csv'.format(ticker))
                    print('Adding new data for {}\n'.format(ticker))
                else:
                    print('Already have {}\n'.format(ticker))
        except:
            print('No data found for {}\n'.format(ticker))
            rmlist.append(ticker)
    # Remove non returning tickers
    for t in rmlist:
        tickers.remove(t)
    with open(picklepath, "wb") as f:
        pickle.dump(tickers, f)


# Create a CSV file out of ticker dataframe
def compile_data(picklepath=None, name=None, comp=True, col_replace='Adj Close'):
    cols = ['High','Low','Open','Close','Volume','Adj Close']
    if comp and col_replace in cols:
        with open(picklepath,'rb') as f:
            tickers = pickle.load(f)
        main_df = pd.DataFrame()
        
        # Loop through tickers and append to csv
        for count, ticker in enumerate(tickers):
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            df.set_index('Date', inplace=True)

            df.rename(columns = {col_replace: ticker}, inplace=True)
            df.drop(df.loc[:, df.columns != ticker].columns, 1, inplace=True)
        
            if main_df.empty:
                main_df = abs(df)
            elif ticker in main_df:
                pass # no instruction if ticker column exists   
            else:
                main_df = main_df.join(abs(df), how='outer')
        
            if count % 25 == 0:
                print('{} / {}'.format(count,len(tickers)))
       
        # Dropping Duplicated Rows
        main_df = main_df.drop_duplicates(keep = False)
        
        #Create CSV file
        main_df.to_csv(name)
        print(main_df.head())
    else:
        print('Have you selected one of {}?'.format(cols))


# Run functions if this is the main script
if __name__ == '__main__':
    # You should compile data on first run, not necesary for subsequent ones 
    # however the data will not update until recompiled.
    collect_tickers_and_compile, COMP = False, False
    
    # Define CSV Filenames
    compilename = 'FTSE250_Compiled.csv'
    compilename_vol = 'FTSE250_TradeVol.csv'          
    
    if collect_tickers_and_compile:
        # Adding additional tickers to tickerlist. Notice that there are
        # repeats. The program will not duplicate these.
        add = ['IAG.L', 'GFS.L', 'BAB.L', 'AJB.L', 'K3C.L', 'CHG.L',
               'EVR.L', 'CNA.L', 'FRAS.L', 'JDW.L', 'MAB.L','IAG.L', 
               'PSN.L', 'K3C.L', 'BOO.L', 'SSE.L', 'REL.L', 'EVR.L',
               'CNA.L', 'JEO.L', 'PHP.L', 'AJB.L', 'BA.L', 'MCX.L']
        
        # Get tickers from wikipedia
        t_filename = 'FTSE250.pickle'
        tickerURL = 'https://en.wikipedia.org/wiki/FTSE_250_Index'
        
        # Get ticker suffixes from Yahoo
        s_filename = 'TickerSuffix.pickle'
        yahooURL = 'https://help.yahoo.com/kb/exchanges-data-providers-yahoo-finance-sln2310.html'
        
        # setup the ticker webscraper function
        YS = Market_Index_TickerList(s_filename, t_filename, yahooURL, tickerURL,
                                     save=True, add_companies=add)
        
        # collect day by day stock data from yahoo (Set reload=True to get new tickers)
        get_data_from_yahoo(reload=True, ticker_funct=YS, picklepath=t_filename, startdate=[2005,1,1])
        
        # compile this information into x1 .csv file for later use and/or reference
        compile_data(picklepath=t_filename , name=compilename)
        
        # compile trade volumes of all the companies into one csv
        compile_data(picklepath=t_filename , name=compilename_vol, col_replace='Volume')
   
    ##################################################################   
    # Are there any specific companies you want to view?
    # (make sure these are in compiled list before requesting to view)
    #view_comps = ['IAG.L', 'GFS.L', 'BAB.L', 'AJB.L', 'K3C.L', 'JDW.L']
    view_comps = None
    
    # Create a CORRELATION TABLE
    #visualize_corr_data(csv_name=compilename, companies=view_comps, clean=True)
    
    # Plot company data/ use interactive plotter
    for i in ['Standardised', 'Percentage Change', 'Price']:
        #time_series_plot(csv_name=compilename, Type=i, companies=view_comps,clean=True, avg=True)
        time_series_plot(csv_name=compilename_vol, Type=i, companies=view_comps,clean=True, avg=True)
     
    # Train Machine Learning Model (change ticker name after looking at above plots)
    tic = 'GFS.L'
    model = tickerML(ticker=tic, requirement=0.02, hm_days=10, comp=COMP)
    #model.run_model()
    
    # Create a candlestick plot for a specific ticker
    #candlestickplot(tic)
    
    # Use below function to look at top/ bottom performing companies
    f1 = 'TV_AC_Dataframe.csv'; f2 = 'PricesDF.csv'
    tradevol_adjclose(TVAJfile=f1, Pfile= f2, showday=100, days=2, TpBt=3)