# Stock Analysis & Machine Learning Model
This project contains a blend of general stock market analysis, data handling/ manipulation, data presentation and finally, machine learning models aimed at predicting day-by-day stock price fluctuations. There are a total of five Python scripts and all of them are required to generate the graphs/ plots that are presented in this *README.md* note. As with the previous project, I will go through the general functionality of each program.

## MAIN.py
As the name suggests, this program is the main script of this project. The user should only have to interface with this script to get any/ all of the outputs displayed in this section. In order to get the most out of this project, the user should become familiar with every single line presented directly below. The reason for this is because almost every uncommented line has some functionality, whether it be to plot a graph, a correlation table, train a machine learning model or otherwise. Let's go through it now.
```Python
# Run functions if this is the main script
if __name__ == '__main__':
    # You should compile data on first run, not necesary for subsequent ones 
    # however the data will not update until recompiled.
    collect_tickers_and_compile, COMP = True, True 
    
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
     
    # Are there any specific companies you want to view?
    # (make sure these are in compiled list before requesting to view)
    #view_comps = ['IAG.L', 'GFS.L', 'BAB.L', 'AJB.L', 'K3C.L', 'JDW.L']
    view_comps = None
    
    # Create a CORRELATION TABLE
    visualize_corr_data(csv_name=compilename, companies=view_comps, clean=True)
    
    # Plot company data/ use interactive plotter
    for i in ['Percentage Change', 'Standardised', 'Price']:
        time_series_plot(csv_name=compilename, Type=i, companies=view_comps,clean=True, avg=False)
        time_series_plot(csv_name=compilename_vol, Type=i, companies=view_comps,clean=True, avg=False)
     
    # Train Machine Learning Model (change ticker name after looking at above plots)
    tic = 'GFS.L'
    model = tickerML(ticker=tic, requirement=0.02, hm_days=10, comp=COMP)
    model.run_model()
    
    # Create a candlestick plot for a specific ticker
    candlestickplot(tic)
    
    # Use below function to look at top/ bottom performing companies
    f1 = 'TV_AC_Dataframe.csv'; f2 = 'PricesDF.csv'
    tradevol_adjclose(TVAJfile=f1, Pfile= f2, showday=100, days=2, TpBt=3)
```
### User Defined Inputs
Although I have given you the option to rename your csv filenames, it is not necessary to do so. A word of caution, changing these filenames between re-runs may crash the program as some of these files are called in differing sections of this project. It is fine to change the names of them but just make sure that you recompile everything afterward to ensure that the appropriate files are generated.

With regards to the weblinks, I do not suggest changing the **yahooURL** link as this directs the program to the official yahoo-finance ticker suffix page. If you prefer to use another index (not FTSE 250 like I have for example), then go ahead and change the weblink for **tickerURL**; just make sure that you select the corresponding stock exchange when prompted in the terminal.
```
# Run functions if this is the main script
if __name__ == '__main__':
    # You should compile data on first run, not necesary for subsequent ones 
    # however the data will not update until recompiled.
    collect_tickers_and_compile, COMP = True, True              <---- USER INPUT
    
    # Define CSV Filenames
    compilename = 'FTSE250_Compiled.csv'
    compilename_vol = 'FTSE250_TradeVol.csv'       
    
    if collect_tickers_and_compile:
        # Adding additional tickers to tickerlist. Notice that there are
        # repeats. The program will not duplicate these.
        add = ['IAG.L', 'GFS.L', 'BAB.L', 'AJB.L', 'K3C.L', 'CHG.L',        <---- USER INPUT
               'EVR.L', 'CNA.L', 'FRAS.L', 'JDW.L', 'MAB.L','IAG.L', 
               'PSN.L', 'K3C.L', 'BOO.L', 'SSE.L', 'REL.L', 'EVR.L',
               'CNA.L', 'JEO.L', 'PHP.L', 'AJB.L', 'BA.L', 'MCX.L']
        
        # Get tickers from wikipedia
        t_filename = 'FTSE250.pickle'
        tickerURL = 'https://en.wikipedia.org/wiki/FTSE_250_Index'
        
        # Get ticker suffixes from Yahoo
        s_filename = 'TickerSuffix.pickle'
        yahooURL = 'https://help.yahoo.com/kb/exchanges-data-providers-yahoo-finance-sln2310.html'
    
    ...
    
    # Are there any specific companies you want to view?
    # (make sure these are in compiled list before requesting to view)
    #view_comps = ['IAG.L', 'GFS.L', 'BAB.L', 'AJB.L', 'K3C.L', 'JDW.L']
    view_comps = None                                                       <---- USER INPUT

    ...

    # Train Machine Learning Model (change ticker name after looking at above plots)
    tic = 'GFS.L'                                                            <---- USER INPUT
```

This project covers two main aspects of 

- the first is general stock market analysis and data handling and the second is using these principles to generate a machine learning model to predict day by day stock price fluctuations.


Overall, running the contents of this folder will create multiple threads which collect ticker data from Yahoo Finance continually, every minute, until stopped by the user. This is an easy script to run from a second computer (Raspberry Pi or Jetson Nano for instance). A .csv file will be generated and then appended every 15 minutes from starting the program. Below is a description of what each of the three Python scripts in this folder do.

## StoreLiveData.py
This is the main script in this folder. Technically speaking, this is the only script that a user will need to interface with, so long as the other two scripts are in the same directory. Lets look at the user input parameters first.

```Python
############# MANUAL PARAMETERS REQUIRED TO BE SET BELOW ################
ticker_no = 250     # define number of tickers being collected -->tickers[0:n]
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
store_weekend = False
####################### END OF MANUAL PARAMETERS #########################
```
All the inputs are commented but a general explination might be necessary here. This program requires a weblink to a wikipedia page containing a ticker list; I have been using is the FTSE 250 in this case. *Note: if there is more than one table on the page, it will automatically search for the correct table and extract the ticker names.*

Since the program pulls ticker data from Yahoo Finance, a *ticker suffix* is required as well. Upon running the script, every single stock market will be displayed as a list in the terminal. The user must select the appropriate stock market. The reason for this is that Yahoo-Finance uses an additional letter code to identify a given ticker (this is based on which stock exchange the company share is traded on). An additional link called **yahooURL** above directs the script to the relevant suffix data. 

So just a quick example, I am webscraping the FTSE 250 list- this will be traded on the London Stock Exchange, therefore I have selected *77* to add the suffix *{ticker}.L* to all my webscraped tickers (which will be used to collect financial data from Yahoo-Finance). 

<img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj1_Webscrape_Min_by_Min/Pictures/request.png" height=500>

Another thing to note here is that stock prices sometimes change over the weekend depending on the stock exchange you are looking at. In my case, stocks are not traded on the weekend so I have set **store_weekend = False**. This will tell the below function to pass *False* back to the main script during out of hours trading rather than *True*. *Note that trading times are defined by the user in the global functions. I would like to webscrape the trading times in a future version of this code however.*

```Python
# Small function to send T/F logic for Exchange Trading Times
def stockmarket_openhours(self, tmzone, O, C, sWE=False):
    ### NOTE: 'state = True': keep updating stock price over weekend  ####
    ### NOTE: 'state = False': stop updating stock price over weekend ####
    store = sWE
    if isinstance(O, list) and isinstance(C, list):
        # Set Market Open/ Close times
        now = datetime.now(tmzone)
        m_open = now.replace(hour=O[0], minute=O[1], second=O[2], microsecond=O[3])
        m_close = now.replace(hour=C[0], minute=C[1], second=C[2], microsecond=C[3])

        # Get day of week (if between 08:30 and 16:30 and weekday then pass True)
        weekday = datetime.now(tmzone).weekday()
        if m_open <= datetime.now(tmzone) <= m_close and weekday <= 4:
            store = True
    else:
        print('\nList not passed to stockmarket_openhours()\n')
    return store
```
## FetchTickers.py
The next section of code contains the functions used to webscrape the tickers and check whether they return valid data. The tickers which pass inspection are passed back to the main script to be used at a later stage (see code for additional information). The section of code below is taken from **StoreLiveData.py**, however, I wanted to introduce the function as it is used in the main script. Notice that the global parameters mentioned earlier are passed here.
```Python
def main(self):
    # Collect list of tickers
    YS = Market_Index_TickerList(self.s_filename, self.t_filename, self.yahooURL, 
                                 self.tickerURL, self.ticker_no, self.save)
    tickers = YS.choose_market()
 ```

## FetchPrice_GithubUpload.py
As the name suggests, this script fetches the live ticker price as well as uploads the data (in a .csv file format) to Github. As fetching a live price for a ticker takes around 1 second and I required to fetch around 250 tickers within a minute, I had to impliment a multi-threading approach to collect the data fast enough. The user may input whatever number of threads they would like into the global parameters displayed earlier (**threads = 10** as seen above) but it is worth noting that adding more threads than your computers' CPU number will not necessarily speed up the data collection. 

Two classes are used in this script:
1. **LivePrice(Thread)**: A threaded approach is required here to ensure that all threads are updating their "work packages/ ticker lists" continually. Effectively, each thread goes through its list and updates the ticker value over and over again.
```Python
# Thread will continually collect workpack finanical data
def run(self):
    if self.tickerlist != None and self.tickerlist != []:
        print('Thread {} has started running\n'.format(self.taskno))
        while not self.terminationRequired:
            for i in range(0, len(self.tickerlist)):
                try:
                    self.ticker_prices[i] = si.get_live_price(self.tickerlist[i])
                except:
                    self.ticker_prices[i] = None
#                        print('----> {} failed...'.format(self.tickerlist[i]))
#                        print("Unexpected error:", sys.exc_info()[0])
#                        raise
    else:
        print('No tickers passed...')
    print('Thread {} has stopped running'.format(self.taskno))
 ```
 
Once the main script requests the values, this script passes the overall ticker list: 
```
# Pull ticker prices from thread
def prices(self):
    return self.ticker_prices
```

2. **class GithubUpdate(Thread)**: When this function is called, code runs through the standard sequence of merging data to this Github repository. This must also be a thread to avoid the main script waiting for the Github upload; this would affect the timer used to count 60 seconds (until the next data collection point).

```Python
def run(self):
    while self.terminationRequired == False:
        if self.trigger == True and os.path.exists(self.filepath):
            os.system("git add {}".format(self.filepath))
            time.sleep(1)
            os.system("git status")
            time.sleep(1)
            os.system("git commit -m 'added'")
            time.sleep(1)
            os.system("git push")
            self.trigger=False
        time.sleep(0.1)
    print('Github thread has stopped running')
```
