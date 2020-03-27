"""
Created on Fri Mar 13 22:57:22 2020

@author: OliverHeilmann

My next task is to webscrape minute by minute data for FTSE 500 companies.
7 days of data should be sufficient here as this is 604,800 total sample which
is likely far more than is required.
"""
import time
import pdb, os
import pandas as pd
from datetime import datetime
from pytz import timezone 
from FetchPrice_GithubUpload import AssignWorkers, GithubUpdate
from FetchTickers import Market_Index_TickerList

############# MANUAL PARAMETERS REQUIRED TO BE SET BELOW ################
ticker_no = 20    # define number of tickers being collected -->tickers[0:n]
threads = 10        # number of threads pulling ticker data (1 per CPU core)
pull_step = 60      # time (60 seconds) between price pull
rows = 15           # number of rows before csv is pushed to Github (1 hour)

# Set Market Open/ Close times (must add the times in)
zone = timezone('Europe/London')    # set the timezone of stock market 
m_open = [8, 0, 0, 0]               # [hour, minute, second, microsecond]
m_close = [16, 30, 0, 0]            # [hour, minute, second, microsecond]
    
# Minute by Minute data collection filename
filename = 'minute_by_minute.csv'

# Get tickers from Wiki URL
t_filename = 'FTSE250.pickle'
tickerURL = 'https://en.wikipedia.org/wiki/FTSE_250_Index'

# Get ticker suffixes from Yahoo
s_filename = 'TickerSuffix.pickle'
yahooURL = 'https://help.yahoo.com/kb/exchanges-data-providers-yahoo-finance-sln2310.html'

save = True
####################### END OF MANUAL PARAMETERS #########################


# Top level functions to store live data
class StoreLiveData:
    def __init__(self, save=True, ticker_no=10, threads=4, pull_step=60,
                     rows=15, zone=timezone('Europe/London'), m_open=[0,0,0,0],
                     m_close=[0,0,0,0], filename=None, t_filename=None, 
                     tickerURL=None, s_filename=None, yahooURL=None):
        
        # Passed parameters in Class
        self.save = save
        self.ticker_no = ticker_no
        self.threads = threads
        self.pull_step = pull_step
        self.rows = rows
        self.zone = zone
        self.m_open = m_open
        self.m_close = m_close
        self.filename = filename
        self.t_filename = t_filename
        self.tickerURL = tickerURL
        self.s_filename = s_filename
        self.yahooURL = yahooURL
        self.ticker_no = ticker_no
        self.save = save
        
        # Setup of dataframe and threads
        self.df = []
        self.AW = AssignWorkers()
        self.GH = GithubUpdate(filepath=self.filename);  
    
    
    # Pull live stock prices and append to dataframe
    def dataframe_prices(self, dataframe):
        if dataframe.size >= 0:
            liveprice = self.AW.pull_live_price()
            # Append dataframe with new data
            if liveprice != [None]:
                self.df.loc[len(self.df)] = liveprice
            return self.df
        else:
            print('No dataframe passed to dataframe_prices')
    
    
    # Small function to send T/F logic for Exchange Trading Times
    def stockmarket_openhours(self, tmzone, O, C):
        if isinstance(O, list) and isinstance(C, list):
            # Set Market Open/ Close times
            now = datetime.now(tmzone)
            m_open = now.replace(hour=O[0], minute=O[1], second=O[2], microsecond=O[3])
            m_close = now.replace(hour=C[0], minute=C[1], second=C[2], microsecond=C[3])
            
            # Get day of week
            weekday = datetime.now(tmzone).weekday()
            if m_open <= datetime.now(tmzone) <= m_close and weekday <= 4:
                return True, m_open, m_close
            return False, m_open, m_close
        else:
            print('\nList not passed to stockmarket_openhours()\n')
            return False, m_open, m_close


    # Main script 
    def main(self):
        # Collect list of tickers
        YS = Market_Index_TickerList(self.s_filename, self.t_filename, self.yahooURL, 
                                     self.tickerURL, self.ticker_no, self.save)
        tickers = YS.choose_market()
        
        # Start webscraping threads
        self.AW.assignworkers(tickerlist=tickers[:self.ticker_no],
                         tickerNo=self.ticker_no, workerNo=self.threads)
        
        # Initiate and start Github thread (required for financial data collection 
        # during github upload)
        self.GH.start()
        self.GH.upload_github()  # ensure Github and script are up to date
        time.sleep(5)
        
        #Main loop giving stock collection instructions
        try:
            while True:
                state, Open, Close = self.stockmarket_openhours(self.zone, self.m_open, self.m_close)
                if state == True:
                    # Make empty dataframe to append to
                    self.df = pd.DataFrame(columns = ['Date Time'] + tickers[:self.ticker_no])
                    
                    # Append price list to dataframe if markets are open
                    for i in range(0,self.rows):
                        # IF statement to check if markets are open
                        if datetime.now(self.zone) <= Close:
                            self.df = self.dataframe_prices(dataframe = self.df)
                            print('Collecting stock prices every {} seconds...'.format(self.pull_step))
                            time.sleep(self.pull_step)
            
                    if not os.path.exists(self.filename):
                        self.df.to_csv(self.filename)
                        print(self.df)
                        print('\n\nCreated filepath...\n{} rows added\n\n'.format(len(self.df)-1))
                        self.GH.upload_github() 
                    else:
                        # Append dataframe to csv file
                        self.df.to_csv(self.filename, mode='a', header=False)
                        print(self.df)
                        print('\nAppended {}...\n{} rows added\b'.format(self.filename, len(self.df)))
                        self.GH.upload_github()
                else:
                    print('Markets are closed...\n')
                    time.sleep(self.pull_step)
        except:
            print('Exiting Main Loop...')
        
        finally:
            # Stop threads when exiting while loop
            self.AW.stop_all()   # stop workers
            self.GH.stop()       # stop Github
            
            # Alert user that collecting has finished
            print('''
                    ###############################\n
                    No more data will be collected.\n
                    ###############################''')


# Main code with governing parameters
if __name__ == '__main__':
    begin = StoreLiveData(save, ticker_no, threads, pull_step, rows, zone,
                          m_open, m_close, filename, t_filename, tickerURL,
                          s_filename, yahooURL)
    begin.main()