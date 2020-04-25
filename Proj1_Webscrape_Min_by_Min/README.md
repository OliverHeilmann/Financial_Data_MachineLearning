# Collect Minute by Minute Stock Data
## Global Parameters
Overall, running the contents of this folder will create multiple threads which collect ticker data from Yahoo Finance continually, every minute, until stopped by the user. This is an easy script to run from a second computer (Raspberry Pi or Jetson Nano for instance). A .csv file will be generated and then appended every 15 minutes from starting the program. Below is a description of what each of the three Python scripts in this folder do:

1. **StoreLiveData.py** is the main script in this folder. Technically speaking, this is the only script that a user will need to interface with (so long as the other two scripts are in the same directory. Lets look at the user input parameters first.

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
All the inputs are commented but a general explination might be necessary here. This program requires a weblink to a wikipedia page containing a ticker list. The one that I have been using is the FTSE 250 list. Don't worry if there is more than one table on the page, it will automatically search for the correct table.
Since the program pulls ticker data from Yahoo Finance, a *ticker suffix* is required as well. Upon running the script, every single stock market will be displayed as a list in the terminal. The user must select the appropriate stock market. The reason for this is that Yahoo-Finance uses an additional letter code to identify a given ticker (this is based on which stock exchange the company share is traded on). An additional link called **yahooURL** above directs the script to the relevant suffix data. So jsut a quick example, I am webscraping the FTSE 250 list- this will be traded on the London Stock Exchange, so I have selected *77* to add the suffix */.L* to all my webscraped tickers (which will be used to collect financial data from Yahoo-Finance). 

<img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj1_Webscrape_Min_by_Min/Pictures/request.png" height=300>
