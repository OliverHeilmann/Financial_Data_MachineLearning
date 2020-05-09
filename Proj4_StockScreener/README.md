# Stock Screnner: A Fundamental Approach to Trading
Building on the works from earlier projects, I have now created a general stock screening tool aimed at finding companies that are undervalued (Value Investing). At the time of writing this, COVID-19 has significantly pulled down stock market values across the world and, as a result, many companies have been deemed to be "undervalued" by the metrics used here. For instance, I noticed that many (almost exlusively) financial and energy sector companies were suggested to be undervalued by this program. Of course, there are larger factors at play here that may disagree with these outputs: 
- What are these sectors going to look like in the future (thinking about renewables vs Crude/LNG)?
- How will global energy consumption change as a result of this pandemic?
- What time scales are we concerned with?
- The list goes on...

Looking more specifically at the contents of this folder, I tried to keep all the code small enough to be in one script. I realised that the previous projects were getting a bit out of hand regarding backward and forward dependencies on scripts- this was becoming a bit challenging for me to debug/ improve/ change parameters, especially with all of them requiring .csv files, .pickle files etc. everywhere. For this project, I made a point to keep it more streamlined so I hope this comes through. I think the best approach to take with this project is to go chronologically through what a user would see in the terminal when first running the script- I will explain some code snippets along the way. As should already be obvious, this stock screener is by no means a silver bullet for trading and was developed exclusively for academic purposes- all of the projects in this Github repository should be treated as such. 

# TickerScraper.py
**Note: that the CollectTickers.py function, developed in Proj2, is used here to collect the users list of tickers.**

## Webscraping: Financial Statistics
The first thing that you will see displayed in the terminal when running this script is text saying *GETTING VALUATION DATA:*. As you might suspect, that is exacly what the first stage of the code is designed to do. The data is pulled from Yahoo (see an example of one of the webpages below). Additionally, the weblink for each ticker being webscraped is printed in the terminal so the user can visit the webpage if needed (*No copywrite infringement intended*).

<p align="center">
  <img height="500" src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj4_StockScreener/Pictures/000Yahoo.png">
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
  <img width="750" src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj4_StockScreener/Pictures/1plot.png">
</p>

### Data Presentation 2:
If further financial information is requested by the user then the following is displayed:
<p align="center">
  <img width="550" src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj4_StockScreener/Pictures/2moreinfo.png">
</p>

### Data Presentation 3:
If even more information is required, the user can request a plot comparing the company stock price to an index- in my case I used FTSE 250 but this can be changed by simply replacing the index='MCX' on the following line of code: 

```Python
# Create a plot of cumulative volume percentage
def cumuVolpcnt(stocklist=[], start='03/01/2020', index='MCX', prices=True):
    # Add index to list
    stocklist.append(index)
```

This section is the one whcih probably needs most work. Ideally, I would like to display other data here such as Force and Market Mommentum which use a combination of stock price and trade volume. The lower plot of the two was an experiment of mine to determine whether any useful information can be extracted from looking at trade volumes for a given time frame (the start date can be changed in the same line of code as above *start='-----'*).

<p align="center">
  <img width="750" src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj4_StockScreener/Pictures/3plot.png">
</p>

## Further Investigation:
Following the narative of this example, we might wish to look into ASIX in more detail after searching through the above information. A simple search on Google shows that ASIX (or AndvanSix) is a chemicals company that manufacture nylon and agricultural fertilisers. In times of high unemployment, industrial sectors are usually a focus for investment as a means of fiscal policy (to create jobs and increase demand). Does the agricultural sector get this attention? If so, ASIX might be a beneficiary of this.

<p align="center">
  <img width="750" src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj4_StockScreener/Pictures/4web.png">
   <img width="750" src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj4_StockScreener/Pictures/5web.png">
</p>

## Outputs
<p align="center">
   <img width="750" src="https://github.com/OliverHeilmann/Financial_Data_MachineLearning/blob/master/Proj4_StockScreener/Pictures/6outputs.png">
</p>

# Final Notes
I did not focus too much on the functionality of the code above as it is fairly straight forward. Some of the other projects have a more detailed description of the code itself but this is probably a product of its complexity. As this project only contained 1 script, I think it is easy to follow the code without too much commentary. 
