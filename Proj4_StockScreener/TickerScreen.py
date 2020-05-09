"""
Created on Tue May  5 20:45:42 2020

@author: OliverHeilmann

VALUE INVESTING STOCK SCREENER
This code uses the CollectTickers.py function to collect a set of tickers (in my
case it was the S&P1000). Adding on this, I have made a value investing stock 
screening program. Effectively, this code collects financial data from yahoo and
looks for companies with high performances in Price/Earnings, PEG and other things.
For the companies which pass this test, an option to display a selection of charts
is presented to the user (along with further data). Additionally, this code saves
the data in csv files saving time on re-runs.

My Notes:
    So I have realised that collecting large quantities of tickers is going
    to take a long time. With a 2 second delay, it will take roughly an hour
    to collect all of the data. It would be fairly straight forward to break
    this task into smaller workpackages and use multithreading. I have already
    done this in Proj1 FetchPrice_GithubUpload.py file so this would only be
    an exercise is saving time rather than learning new skills. For those who
    want to apply multithreading, I suggest looking at that file. For now, 
    I will kill the time making dinner.
    
    I noticed was that Yahoo refused my requests if no delay was added to the 
    webscraping functions. I added in a two second sleep function which has
    remedied this issue.
"""
import requests
import bs4 as bs
import pandas as pd
import pickle
from string import digits
import datetime as dt
from yahoo_fin.stock_info import get_data
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from CollectTickers import Market_Index_TickerList
import quandl
from datetime import datetime as dt
import numpy as np
import pdb, os
import copy
from matplotlib import style
import time
style.use('ggplot')
rcParams['figure.figsize'] = 12,8

'''
Plotting:
    %matplotlib qt        --> as po-pup
    %matplotlib inline    --> in shell
'''

'''
To be used later:
    import quandl
    quandl.ApiConfig.api_key = 'YOUR QUANDL KEY HERE'
    mydata = quandl.get('EURONEXT/ADYEN', ticker=stock[:-2], start_date='2010-05-05', end_date='2020-05-05')
    mydata.plot()
'''

#def getQuandl(stock='AAPL'):
#    quandl.ApiConfig.api_key = '9baucNgmhMRN9hpsJDE3'
#    #data = quandl.get_table('ZACKS/FC', paginate=True, ticker='AAPL', qopts={'columns': ['ticker', 'per_end_date']})
#    
#    data = quandl.get_table("ZACKS/FC", paginate=True)
#    #mydata = quandl.get_table('ZACKS/FC', ticker=stock, start_date='2010-01-01', end_date='2020-05-05')
#    
#    #mydata = quandl.get('EURONEXT/ADYEN', ticker=goldlist[0], start_date='2010-05-05', end_date='2020-05-05')
#    return data


# Create a plot of cumulative volume percentage
def cumuVolpcnt(stocklist=[], start='03/01/2020', index='MCX', prices=True):
    # Add index to list
    stocklist.append(index)
    
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('CUMULATIVE VOLUME %CHANGE', size=20)
    
    ax1 = plt.subplot2grid((11,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((11,1), (6,0), rowspan=5, colspan=1, sharex=ax1)
    ax1.xaxis_date()
     
    ax1.set(ylabel='PRICE ({} index)'.format(index))
    ax2.set(ylabel='CUMULATIVE SUM %')
    
    for stock in stocklist:    
        # Get ticker data from yahoo in date range
        df = get_data(stock, start_date=start)
        
        # Create Cumulative Sum % increase column in df
        df['cum_sum'] = df['volume'].cumsum()
        df['{}_Cumu%'.format(stock)] = df['cum_sum']/df['volume'].sum()
        
        if prices or stock == index:
            # Potentially don't want multiple stocks displayed here
            ax1.plot(df.index, df['adjclose'], label=stock)
        ax2.plot(df.index, df['{}_Cumu%'.format(stock)], label=stock)
    
    # Straight line for reference
    x = [df.index[0], df.index[-1]]; y = [0,1 ]
    nums = {'Date': x,'Reference': y}
    line = pd.DataFrame(nums, columns = ['Date', 'Reference']).set_index('Date')
    #print(main_df.join(line).head())
    
    # Plotting data
    ax2.plot(line.index, line, linewidth=4, label='Reference') # reference line
    
    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right')
    plt.show()


# Get Valuation Metrics from Yahoo
def valuationDF(stocklist=['AAPL'], update=True):
    # Save as csv in case we need later
    if not os.path.exists('ValuationDataFrame.csv') or update:
        main_df = pd.DataFrame()
        print('\nGETTING VALUATION DATA:')
        
        # In case there are any leading/ trailing spaces
        stocklist = [i.strip() for i in stocklist]
        for stock in stocklist:
            try:
                # Sleep is needed otherwise Yahoo starts to refuse connection
                time.sleep(2)
                
                # Lets print percentage complete for user information
                pct_stat = round((stocklist.index(stock)+1)*100/len(stocklist),1)
                
                yahooURL = 'https://finance.yahoo.com/quote/'+stock+'/key-statistics?ltr=1'
                print(f'    {pct_stat}% {stock} --> {yahooURL}')
    
                # Fetch Ticker information from Yahoo
                resp = requests.get(yahooURL)
                soup = bs.BeautifulSoup(resp.text, 'html.parser') # or lxml
                
                # Get all available data from yahoo for dataframe
                full_df = pd.DataFrame()
                for table in soup.find_all('table'):
                    data = [ele.text.strip() for ele in table.find_all('td')] 
                    titles = [k.strip() for k in data if data.index(k) %2 ==0]
                    values = [k for k in data if data.index(k) %2]
    
                    # Make Dataframe of extracted values
                    nums = {'Valuation Measures': titles,'{}'.format(stock): values}
                    df = pd.DataFrame (nums, columns = ['Valuation Measures', '{}'.format(stock)])
    
                    # Append ticker data to global dataframe            
                    if len(full_df)==0:
                        full_df = df
                    else:
                        full_df = full_df.append(df)
                        
                full_df.reset_index(inplace=True)
                full_df.drop('index', axis=1, inplace=True)
    
                # Append ticker data to global dataframe            
                if len(main_df)==0:
                    main_df = full_df
                else:
                    main_df = main_df.join(full_df['{}'.format(stock)])
            
            except Exception as E:
                print(f'\n{stock}: {E}. Likely no data on Yahoo!\n')
        
        # Getting rid of trailing numbers (leftover footnotes)
        for i, el in enumerate(main_df['Valuation Measures']):
            if el[-1] in digits:
                main_df['Valuation Measures'].iloc[i] = main_df['Valuation Measures'].iloc[i][:-1]
            main_df['Valuation Measures'].iloc[i].strip()
            
        # Set Valuation Measures as the index
        main_df.set_index("Valuation Measures", inplace=True)
        
        # Create csv file with data
        main_df.to_csv('ValuationDataFrame.csv')
        print('Created ValuationDataFrame')
    
    else:
        print('READING IN ValuationDataFrame...')
        main_df = pd.read_csv('ValuationDataFrame.csv')
       
        # Set Valuation Measures as the index
        main_df.set_index("Valuation Measures", inplace=True)
    return main_df


# Convert cells in dataframe to numbers (or NaNs)
def dfnumerize(dataframe):
    dataframe = dataframe.iloc[:,:].replace('-','0')
    dataframe = dataframe.iloc[:,:].replace(np.nan,'')
    dataframe = dataframe.apply(lambda x: x.str.replace(',', ''), axis=1)
    dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
    return dataframe


# Get Key Financial Metrics from Yahoo
def financialDF(stocklist=['AAPL', 'TXG'], update=True):
    # Save as csv in case we need later
    if not os.path.exists('Financials/RevenueDataFrame.csv') or update:
        print('\nGETTING FUNDAMENTAL DATA:')
        
        # In case there are any leading/ trailing spaces
        stocklist = [i.strip() for i in stocklist]
        for stock in stocklist:
            try:
                # Sleep is needed otherwise Yahoo starts to refuse connection
                time.sleep(2)
                
                # Lets print percentage complete for user information
                pct_stat = round((stocklist.index(stock)+1)*100/len(stocklist),1)

                yahooURL = 'https://finance.yahoo.com/quote/'+stock+'/financials?p='+stock
                print(f'    {pct_stat}% {stock} --> {yahooURL}')
                
                # Fetch Ticker information from Yahoo
                resp = requests.get(yahooURL)
                soup = bs.BeautifulSoup(resp.text, 'html.parser') # or lxml
                
                ######## NOTE: THIS SECTION PULLS ALL DATA FROM PAGE ########
                # Extract text (as rows) from soup 
                allData = soup.findAll("div", {"class": "D(tbr)"})
                
                if allData != []:
                    tabledata = []
                    for row in allData:
                        rowdata = []
                        for el in row:
                            rowdata.append(el.text)
                        tabledata.append(rowdata)
                else:
                    print(f'\nDataset not found for {stock}: _________\n')
                    continue
                
                # Put all data collected in dataframe
                df = pd.DataFrame(tabledata)
                df.columns = df.iloc[0]
                df = df.drop(df.index[0])
                df = df.reset_index(drop=True)
                
                # Get row index of the information we want (sometimes differs)
                ints = []; trigger = False
                DATA = ['Total Revenue', 'Gross Profit', 'Net Income Common Stockholders']
                for el in DATA:
                    try:
                        ints.append(df.loc[df['Breakdown'] == el].index[0])
                    except:
                        trigger = True
                        print(f'\nDataset not found for {stock}: No {el}\n')
                        break
              
                # If data was not found we skip the ticker
                if trigger:
                    continue
                
                # Set index to Breakdown column
                df.set_index('Breakdown', inplace=True)
                #############################################################
                
                # Append ticker data to global dataframes           
                if stocklist.index(stock)==0:                    
                    # Make Total Profit DF
                    rev_df = pd.DataFrame(df.iloc[ints[0]])
                    rev_df.rename(columns={DATA[0]:'{}'.format(stock)}, inplace=True)
                    
                    # Make Gross Profit DF
                    grossp_df = pd.DataFrame(df.iloc[ints[1]])
                    grossp_df.rename(columns={DATA[1]:'{}'.format(stock)}, inplace=True)
                    
                    # Make Net Income DF
                    netinc_df = pd.DataFrame(df.iloc[ints[2]])
                    netinc_df.rename(columns={DATA[2]:'{}'.format(stock)}, inplace=True)
                    
                else:
                    # Merge Total Profit DF
                    t1 = pd.DataFrame(df.iloc[ints[0]])
                    rev_df = pd.concat([rev_df, t1], axis=1, sort=True)
                    rev_df.rename(columns={rev_df.columns[-1]:'{}'.format(stock)}, inplace=True)
                    
                    # Merge Gross Profit DF
                    t2 = pd.DataFrame(df.iloc[ints[1]])
                    grossp_df = pd.concat([grossp_df, t2], axis=1, sort=True)
                    grossp_df.rename(columns={grossp_df.columns[-1]:'{}'.format(stock)}, inplace=True)
                    
                    # Merge Net Income DF
                    t3 = pd.DataFrame(df.iloc[ints[2]])
                    netinc_df = pd.concat([netinc_df, t3], axis=1, sort=True)
                    netinc_df.rename(columns={netinc_df.columns[-1]:'{}'.format(stock)}, inplace=True)
            
            except Exception as E:
                print(f'{E}: Yahoo connection potentially refused!')
        
        # Replace 'total to month with date today
        now = dt.now()
        rev_df.rename(index={'ttm': now}, inplace=True)
        grossp_df.rename(index={'ttm': now}, inplace=True)
        netinc_df.rename(index={'ttm': now}, inplace=True)
    
        # Convert date strings to datetime format
        for ind in range(0, rev_df.shape[0]-1):
            i1 = rev_df.index[ind]
            rev_df.rename(index={i1:dt.strptime(i1, '%m/%d/%Y')}, inplace=True)
       
            i2 = grossp_df.index[ind]
            grossp_df.rename(index={i2:dt.strptime(i2, '%m/%d/%Y')}, inplace=True)
        
            i3 = netinc_df.index[ind]
            netinc_df.rename(index={i3:dt.strptime(i3, '%m/%d/%Y')}, inplace=True)
    
        # And finally chronologically re-order indexes
        rev_df.sort_index(inplace=True)
        grossp_df.sort_index(inplace=True)
        netinc_df.sort_index(inplace=True)
        
        rev_df = dfnumerize(rev_df)
        grossp_df = dfnumerize(grossp_df)
        netinc_df = dfnumerize(netinc_df)
        
        # Create csv files with data
        if not os.path.exists('Financials'):
            os.makedirs('Financials')
        rev_df.to_csv('Financials/RevenueDataFrame.csv')
        grossp_df.to_csv('Financials/ProfitDataFrame.csv')
        netinc_df.to_csv('Financials/IncomeDataFrame.csv')
        print('Created CSV files from dataframes')
    
    else:
        print('READING IN Financial DataFrames...')
        rev_df = pd.read_csv('Financials/RevenueDataFrame.csv')
        rev_df.set_index('Unnamed: 0', inplace=True)
        
        grossp_df = pd.read_csv('Financials/ProfitDataFrame.csv')
        grossp_df.set_index('Unnamed: 0', inplace=True)
        
        netinc_df = pd.read_csv('Financials/IncomeDataFrame.csv')
        netinc_df.set_index('Unnamed: 0', inplace=True)
    
    return rev_df, grossp_df, netinc_df


# Plot the data collected from the Financials folder
def plotFunds(ticker, revenueDF, grossprofitDF, netincomeDF):
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle(f'{ticker}: TOTAL REVENUE, GROSS PROFIT AND NET INCOME PLOTS', size=25)

    ax1 = plt.subplot2grid((17,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((17,1), (6,0), rowspan=5, colspan=1, sharex=ax1)
    ax3 = plt.subplot2grid((17,1), (12,0), rowspan=5, colspan=1, sharex=ax1)
    ax1.xaxis_date()
     
    # Assign Axes
    ax1.set(ylabel='Revenue (USD)')
    ax2.set(ylabel='Gross Profit (USD)')
    ax3.set(xlabel='Date', ylabel='Net Income (USD)')
    
    # Add note/ subtitle
    ax1.title.set_text('''
Note: If Revenue and Gross Profit plots look the same it is because no 
data was available for Gross Profit. This will be fixed in the future...''')
    
    # Drop NaN rows to plot lines after
    rdf = revenueDF[ticker].dropna()
    gdf = grossprofitDF[ticker].dropna()
    idf = netincomeDF[ticker].dropna()
    
    # Plot data for specific ticker only
    for i, val in zip([ax1, ax2, ax3],[rdf, gdf, idf]):
        if val.sum() >= 0:
            i.plot_date(val.index, val, ls='-', color='green')
        else:
            i.plot_date(val.index, val, ls='-', color='red')
    plt.show()
    
    
# Do preliminary screen on passed dataframe
def prelimScreen(df, rev_df, grossp_df, netinc_df):
    print('-------RUNNING STOCK SCREENER--------\n')
    # Clean dataframe. This gets rid of % and billions so must update
    # at some point. Not important at the moment as we do not use these
    # values anyway...
    mydata = copy.deepcopy(df)
    df = dfnumerize(df)
    
    pbr = df.iloc[6]
    peg = df.iloc[4]
    tpe = df.iloc[2]
    tde = df.iloc[-5]
    
    for ind, v1, v2, v3, v4 in zip(df.columns, pbr, peg, tpe, tde):
        try:
            #print(f'{ind}: {v1}, {v2}, {v3}, {v4}')
            # Should be v1 < 1, v2 < 1, v3 < 13, v4-->N/A
            if float(v1)<1 and 0<float(v2)<1 and float(v3)<13:
                print(f'''
{ind} meets requirements:
-->Price to Book: {v1}
-->PEG (5 year): {v2}
-->Trailing PE: {v3}
-->Debt Equity: {v4}''')
                # Collecting data between two pages might be asymetric
                if ind in rev_df.columns:
                    ans = input('Show financial charts? (y/n)').lower()
                    if ans == 'y':
                        # Plot the collected data for a specific ticker
                        plotFunds(ind, rev_df, grossp_df, netinc_df)
                        ans = input('Show more info? (y/n)').lower()
                        if ans == 'y':
                            print(mydata[ind])
                        ans = input('Show cumulative volume %change? (y/n)').lower()
                        if ans == 'y':
                            try:
                                # Call cumulative volume % function
                                cumuVolpcnt(stocklist=[ind], start='03/01/2020', prices=True)
                            except:
                                print('Unofrtunately, no data available.')
        except Exception as E:
            print(f'\n{ind}: {E}. {ind} likely operating in the red.\n')


# Run if the main script
if __name__ == '__main__':            
    # setup the ticker webscraper function (using old webscraping code)
    if not os.path.exists('SP1000.pickle'):
        # Get tickers from wikipedia
        t_filename = 'SP1000.pickle'
        tickerURL = 'https://en.wikipedia.org/wiki/List_of_S%26P_1000_companies'
            
        # Get ticker suffixes from Yahoo
        s_filename = 'TickerSuffix.pickle'
        yahooURL = 'https://help.yahoo.com/kb/exchanges-data-providers-yahoo-finance-sln2310.html'
        
        # Now call the function to get tickers
        YS = Market_Index_TickerList(s_filename, t_filename, yahooURL, tickerURL, save=True)
        tickers = YS.choose_market()
    else:
        with open('SP1000.pickle', "rb") as f:
            tickers = pickle.load(f)

    # List of some interesting Gold companies
    goldlist = ['AUY', 'GOLD', 'KGC', 'NG', 'TXG']
    
    # IF YOU CHANGE LIST YOU MUST UPDATE DATAFRAMES (update=True)
    passlist = tickers[220:240] # I only want 20 tickers (of 1000) for demonstration

    # Collect Yahoo Fundamental tickerlist data
    dataframe = valuationDF(stocklist=passlist, update=True)
    
    # Get Revenue, Gross Profit, Net Income data for all tickers
    rev_df, grossp_df, netinc_df = financialDF(stocklist=passlist, update=True)

    # Perform preliminary screen using dataframe data
    prelimScreen(dataframe, rev_df, grossp_df, netinc_df)
    
    # Call cumulative volume % function and plot data (separate project)
    #cumuVolpcnt(stocklist=passlist[3:8], start='01/01/2020')
    
    #data = getQuandl()
    #print(data)
