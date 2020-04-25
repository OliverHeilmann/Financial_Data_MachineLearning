# Stock Analysis & Machine Learning Model
This project contains a blend of general stock market analysis, data handling/ manipulation, data presentation and finally, machine learning models aimed at predicting day-by-day stock price fluctuations. There are a total of five Python scripts and all of them are required to generate the graphs/ plots that are presented in this *README.md* note. As with the previous project, I will go through the general functionality of each program.

## MAIN.py
As the name suggests, this program is the main script of this project. The user should only have to interface with this script to get any/ all of the outputs displayed in this section. In order to get the most out of this project, the user should become familiar with every single line presented directly below. The reason for this is because almost every uncommented line has some functionality, whether it be to plot a graph, a correlation table, train a machine learning model or otherwise. Let's go through it now.
```Python
# Run functions if this is the main script
if __name__ == '__main__':
    # You should compile data on first run, not necesary for subsequent ones 
    # however the data will not update until recompiled.
    collect_tickers_and_compile, COMP = True, True                   #<---- USER INPUT HERE
    
    # Define CSV Filenames
    compilename = 'FTSE250_Compiled.csv'
    compilename_vol = 'FTSE250_TradeVol.csv'       
    
    if collect_tickers_and_compile:
        # Adding additional tickers to tickerlist. Notice that there are
        # repeats. The program will not duplicate these.
        add = ['IAG.L', 'GFS.L', 'BAB.L', 'AJB.L', 'K3C.L', 'CHG.L',         #<---- USER INPUT HERE
               'EVR.L', 'CNA.L', 'FRAS.L', 'JDW.L', 'MAB.L','IAG.L', 
               'PSN.L', 'K3C.L', 'BOO.L', 'SSE.L', 'REL.L', 'EVR.L',
               'CNA.L', 'JEO.L', 'PHP.L', 'AJB.L', 'BA.L', 'MCX.L']
        
        # Get tickers from wikipedia
        t_filename = 'FTSE250.pickle'
        tickerURL = 'https://en.wikipedia.org/wiki/FTSE_250_Index'           #<---- USER INPUT HERE
        
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
    #view_comps = ['IAG.L', 'GFS.L', 'BAB.L', 'AJB.L', 'K3C.L', 'JDW.L']         #<---- USER INPUT HERE
    view_comps = None
    
    # Create a CORRELATION TABLE
    visualize_corr_data(csv_name=compilename, companies=view_comps, clean=True)
    
    # Plot company data/ use interactive plotter
    for i in ['Percentage Change', 'Standardised', 'Price']:
        time_series_plot(csv_name=compilename, Type=i, companies=view_comps,clean=True, avg=False)
        time_series_plot(csv_name=compilename_vol, Type=i, companies=view_comps,clean=True, avg=False)
     
    # Train Machine Learning Model (change ticker name after looking at above plots)
    tic = 'GFS.L'                                                                        #<---- USER INPUT HERE
    model = tickerML(ticker=tic, requirement=0.02, hm_days=10, comp=COMP)
    model.run_model()
    
    # Create a candlestick plot for a specific ticker
    candlestickplot(tic)
    
    # Use below function to look at top/ bottom performing companies
    f1 = 'TV_AC_Dataframe.csv'; f2 = 'PricesDF.csv'
    tradevol_adjclose(TVAJfile=f1, Pfile= f2, showday=100, days=2, TpBt=3)
```
### User Defined Inputs
Although I have given you the option to rename your csv and pickle filenames (see *compilename, compilename_vol, t_filename, s_filename, f1 and f2*), it is not necessary to do so. A word of caution, changing these filenames between re-runs may crash the program as some of these files are called in differing sections of this project. It is fine to change the names of them but just make sure that you recompile everything afterward to ensure that the appropriate files are generated with the names you want.

With regards to the weblinks, I do not suggest changing the **yahooURL** link as this directs the program to the official yahoo-finance ticker suffix page. If you prefer to use another index (not FTSE 250 like I have for example), then go ahead and change the weblink for **tickerURL**; just make sure that you select the corresponding stock exchange when prompted in the terminal. 

So just a quick example, I am webscraping the FTSE 250 list- this will be traded on the London Stock Exchange, therefore I have selected *77* to add the suffix *'{ticker}.L'* to all my webscraped tickers (which will be used to collect financial data from Yahoo-Finance). 

<img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj1_Webscrape_Min_by_Min/Pictures/request.png" height=500>

### Compiling Ticker Data
Ok so this is quite important- make sure you compile everything on your first run (i.e. set to ***= True, True***) or when you change the names of your files. 
```Python
# You should compile data on first run, not necesary for subsequent ones 
# however the data will not update until recompiled.
collect_tickers_and_compile, COMP = True, True                   #<---- USER INPUT HERE
```
If you ever want to update your dataset/ keep your ticker prices up to date, just recompile the data again- the new information will be appended to the files you already have. Something like the image below will be displayed in your terminal. These files will be saved under the **stocks_dfs** directory.

- If there is no ticker file: *'Created file for {ticker} data'*
- If the ticker file already exists: *'Adding new data for {ticker}'*
- If you already have ticker: *'Already have {ticker}'*

## CollectTickers.py
I won't go through the details of how the tickers are collected again as this is pretty well documented in the **README.md** file in **Proj1_...**. It is, in effect, the same thing as before with a few improvements. Additionally, it is organised under a *Class* which is better coding practice. The intention here was to be able to call this function in future programs as well as this one. I did however add the functionality do add additional companies to the ticker list- simply add the ticker (with the correct suffix) into the list indicated below and the relevant ticker data will be websrcaped and compiled along with the index you have provided in the Wikipedia link (see *tickerURL*).
```Python
if collect_tickers_and_compile:
    # Adding additional tickers to tickerlist. Notice that there are
    # repeats. The program will not duplicate these.
    add = ['IAG.L', 'GFS.L', 'BAB.L', 'AJB.L', 'K3C.L', 'CHG.L',         #<---- USER INPUT HERE
           'EVR.L', 'CNA.L', 'FRAS.L', 'JDW.L', 'MAB.L','IAG.L', 
           'PSN.L', 'K3C.L', 'BOO.L', 'SSE.L', 'REL.L', 'EVR.L',
           'CNA.L', 'JEO.L', 'PHP.L', 'AJB.L', 'BA.L', 'MCX.L']

    ...

    # setup the ticker webscraper function
    YS = Market_Index_TickerList(s_filename, t_filename, yahooURL, tickerURL, save=True, add_companies=add)
```

## InteractivePlotter.py
This script outputs a Correlation Table as well as a series of figures presenting Trade Volume and/or Stock Price data (either as a Percentage Change/ Day, Standardised, or Stock Price) for all the tickers you have selected and compiled.

### Correlation Table: visualize_corr_data()
If you would like to produce a correlation table from the ticker list you have defined, simply leave this line of code uncommented.
```Python
# Create a CORRELATION TABLE
visualize_corr_data(csv_name=compilename, companies=view_comps, clean=True)
```
**What does a correlation table actually represent?** Simply put, it shows the similarity of company data with one another. If two companies stock prices rise and fall together frequently, they are considered to be similar and would have a score closer to 1.0 (green). The opposite is true for disimilar companies (red).
<p float="left">
  <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/CorrPlot.png" height=300 />
  <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/CorrPlot2.png" height=300 />
</p>
As with all of the plots presented here, the user is able to navigate around the tables/ graphs freely and zoom in on the companies they are interested in. This output alone people actually pay money for online so having this functionality for free is quite useful here. 

### Price, Standardise, Percent Change: visualize_corr_data()

<p float="left">
  <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/StockPrices.png" height=300 />
 <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/stndard.png" height=300 />
</p>




