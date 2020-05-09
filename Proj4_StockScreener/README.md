# Stock Screnner: A Fundamental Approach to Trading
Building on the works from earlier projects, I have now created a general stock screening tool aimed at finding companies that are undervalued (Value Investing). At the time of writing this, COVID-19 has significantly pulled down stock market values across the world and, as a result, many companies have been deemed to be "undervalued" by the metrics used here. For instance, I noticed that many (almost exlusively) financial and energy sector companies were suggested to be undervalued by this program. Of course, there are larger factors at play here that may disagree with these outputs: 
- What are these sectors going to look like in the future (thinking about renewables vs Crude/LNG)?
- How will global energy consumption change as a result of this pandemic?
- What time scales are we concerned with?
- The list goes on...

Looking more specifically at the contents of this folder, I tried to keep all the code small enough to be in one script. I realised that the previous projects were getting a bit out of hand regarding backward and forward dependencies on scripts- this was becoming a bit challenging for me to debug/ improve/ change parameters, especially with all of them requiring .csv files, .pickle files etc. everywhere. For this project, I made a point to keep it more streamlined so I hope this comes through. I think the best approach to take with this project is to go chronologically through what a user would see in the terminal when first running the script- I will explain some code snippets along the way. As should already be obvious, this stock screener is by no means a silver bullet for trading and was developed exclusively for academic purposes- all of the projects in this Github repository should be treated as such. 

# TickerScraper.py 
## Webscraping: Financial Statistics
The first thing that you will see displayed in the terminal when running this script is text saying *GETTING VALUATION DATA:*. As you might suspect, that is exacly what the first stage of the code is designed to do. The data is pulled from Yahoo (see an example of one of the webpages below). Additionally, the weblink for each ticker being webscraped is printed in the terminal so the user can visit the webpage if needed (*No copywrite infringement intended*).

<p align="center">
  <img height="400" src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj4_StockScreener/Pictures/000Yahoo.png">
</p>

I noticed was that Yahoo refused my requests if no delay was added to the webscraping functions. I added in a two second sleep function which has remedied this issue. With a 2 second delay, it will take roughly an hour to collect all of the data for the S&P 1000 (I appreciate that you may wish to use a different ticker list). It would be fairly straight forward to break this task into smaller workpackages and use multithreading. I have already done this in Proj1 FetchPrice_GithubUpload.py file so this would only be an exercise is saving time rather than learning new skills. For those who want to apply multithreading, I suggest looking at that file. Below is an example of what a user might see in their terminal.

<p float="left">
  <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj4_StockScreener/Pictures/0CollectData.png" width=535 />
 <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj4_StockScreener/Pictures/00CollectData.png" width=365 />
</p>

The final point here would be that Yahoo has a very inconsistently populated webpage which makes it quite difficult to collect specific information. As a means of error handling, I have dropped all the tickers which do not return the information that I am scanning for.

## Stock Screen:
For this section, it is worth having a look at the code to see what is going on *under the hood*. As you can see from this code, there are a series of *if* statements and user *inputs* which determine what level of information is given to the user.

```Python
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
                      -->Debt Equity: {v4}
                      ''')
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
```

If the following conditions are met, then the user will be prompted if they would like further information on the company:
- Price to Book < 1
- 0 < PEG (5 year) < 1
- Trailing Price/Earnings < 13
- Debt Equity has no requirement currently

See the following section of code:
```Python
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
                      -->Debt Equity: {v4}
                      ''')
```
### Data Presentation 1:
Upon finding a company that has met the requirments, the user is prompted whether they would like more information. If their input is *y* then the following is displayed.
<p align="center">
  <img width="600" src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj4_StockScreener/Pictures/1plot.png">
</p>

### Data Presentation 2:
### Data Presentation 3:

## Further Investigation:

# Final Outputs

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

### Price, Standardise, Percent Change: time_series_plot()
This function outputs x3 graphs using the ticker data compiled into csv format. Notice that the fuction is repeated twice- the first is for the stock prices, and the second is for the trade volumes. The *for loop* is used to generate a total of 6 graphs. A'Percentage Change', 'Standardised' and 'Price' for both the stock prices and trade volumes.
```Python
# Plot company data/ use interactive plotter
for i in ['Percentage Change', 'Standardised', 'Price']:
    time_series_plot(csv_name=compilename, Type=i, companies=view_comps,clean=True, avg=False)
    time_series_plot(csv_name=compilename_vol, Type=i, companies=view_comps,clean=True, avg=False)
```
Below is an illustration of the kind of output seen. An additional note is that the user can identify which line relates to which company by simply moving the mouse over the line in question. A pop-up box will appear with the ticker name (see below). On top of this, **avg=True** will plot an average line on the graph as well; this can be seen below as the thick red line.
<p float="left">
  <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/StockPrices.png" height=300 />
 <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/stndard.png" height=300 />
</p>

## MovingAverage.py
This script contains two functions which can plot two separate outputs. See the code below for the function names.
```Python
tic = 'GFS.L'                                                                        #<---- USER INPUT HERE

...

# Create a candlestick plot for a specific ticker
candlestickplot(tic)

# Use below function to look at top/ bottom performing companies
f1 = 'TV_AC_Dataframe.csv'; f2 = 'PricesDF.csv'
tradevol_adjclose(TVAJfile=f1, Pfile= f2, showday=100, days=2, TpBt=3)
```

### CandleStick Graph: candlestickplot()
This function will plot a candlestick chart for whichever ticker you input (must be from the original list you compiled however). Additionally, a 100 day and 20 day moving average will be displayed for your data in yellow and blue respectively. Furthermore, a subplot with the trade volume is displayed. As the user zooms in on sections, the trade volume automatically moves as well.
<p float="left">
  <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/GFS_Candlestick.png" height=300 />
 <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/GFS_Candlestick2.png" height=300 />
</p>


### [Trade Volume/ Adjusted Close]% Change/Day: tradevol_adjclose()
This function centres around the [Trade Volume/ Adjusted Close]% Change/Day information which I have found to be a better metric than simply analysing stock price data. As trade volume goes up, we can assume that interest in the company also increases. If the Adjusted Close price has gone down in value in the same day, then the fraction *Trade Volume/ Adjusted Close* increases. We monitor the percentage change per day to see when the optimal time to buy the stock is (when trading volume is higher than normal and adjusted close is lower than normal).

The information presented in the table below shows the TOP X and BOTTOM X performing companies averaged over the PAST Y DAYS. If the [TV/AC]% value is high, then it is likely a good time to buy shares in that ticker, the opposite is true for a low [TV/AC]%. Trade volumes are quite volotile (as are stock prices, especially during the COVID-19 pandemic) so I suggest using an average of around 3 days maximum if you plan on buying/ selling shares in short time periods.

Another interesting thing to note is that the [TV/AC]% peaks often align with one another- I suspect this is an indication into where the *market interest* lies on a given time period. My intention is to use this data format to feed into a machine learning model.

<img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/TopBot_CompaniesChart.png" height=700>

## VolPrice_ML.py
This script is the machine learning aspect of this project. Here, I have used a *Supervised Classification* method of training rather than a *Regression* (though I will be experimenting with this later). The code below calls the ML training function for which ever ticker is input by the user. If you do not wish to train a model, simply comment out the **model.run_model()** line.
```Python
# Train Machine Learning Model (change ticker name after looking at above plots)
tic = 'GFS.L'                                                                        #<---- USER INPUT HERE
model = tickerML(ticker=tic, requirement=0.02, hm_days=10, comp=COMP)
model.run_model()
```
The way this function works is by setting a threshold %change in Adjusted Close price (**requirement=0.02** here). If the stock price increases by more than **2%** in **10** days (see **hm_days=10**) then this is a *BUY*. If it goes down by **2%** or more then it is a *SELL*; otherwise it is a *HOLD*. I use this decision to add an additional column to a *Pandas Dataframe* with BUY=1, SELL=-1, HOLD=0 on each row. See the code below.
```Python
# Turning this into a classification problem (not regression)
def buy_sell_hold(self, *args):
    # Each time this function is called, 'x' next days of values are
    # passed through this for loop. As soon as the requirement is met,
    # a value will be returned.
    cols = [c for c in args]
    for col in cols:
        if col > self.requirement:
            return 1
        if col < -self.requirement:
            return -1
    # If not buy or sell then hold
    return 0
```
For the classification model I use an ensemble voting classifier with KNN and Random Forest Classifiers as these seemed to give the best results; SVM for example actually reduced the overall accuracy of the model for example (however this is perhaps because it was producing a more accurate fit to the data perhaps). 

```Python
# Keep dataset for final validation after ML
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

...

# Ensemble Voting Classifier
clf = VotingClassifier([('knn', neighbors.KNeighborsClassifier(n_neighbors=5, n_jobs=-1)),
                        ('rfor', RandomForestClassifier(min_samples_leaf=150))])    

# Fit Data (i.e. do the machine learning)
clf.fit(X_train, y_train)
```
I optimised the input parameters for the KNN and RF classifier models- here is an example:
<img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/RF_Optimised.png" height=600>

Finally, I fit the model and make predictions on a test dataset (see **train_test_split**). The green dots indicate *BUY* predictions, red are *SELL* and black are *HOLD* as illustrated in the legend. Accuracies are presented in the title; in this case it was **42%** for GFS which is not too bad considering the type of data I was using and the simple approach taken. The accuracy here was actually increased significantly after only applying the [TV/AC]% approach mentioned earlier (from around 36% average accuracy before). 
<p float="left">
  <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/BA_ML_Predictions.png" height=300 />
 <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/BA_ML_Predictions2.png" height=300 />
</p>
If I revisit this in the future, I would like to use the correlation table data to suggest highly correlated companies to use in the ML model (rather than all of them which undoubtedly causes confusion in the model). Combining this with moving average data might further increase the accuracy- I suspect that this can be increased to around 50% without requiring a neural network for example.

## Final Notes
After successfully running the main script you will have produced the following files. Note that the ML model has also been pickled for use at a later date if required.
 <img src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj2_DataAnalysis_ML/Pictures/createdfiles.png" height=300>
