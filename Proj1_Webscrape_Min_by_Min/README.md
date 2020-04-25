# Collect Minute by Minute Stock Data
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
