#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:49:47 2020

@author: OliverHeilmann
"""
import numpy as np
import pandas as pd
import pickle, os, pdb
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn import svm, neighbors

'''
use:
    %matplotlib qt        --> as po-pup
    %matplotlib inline    --> in shell
'''
class tickerML:
    def __init__(self, ticker=None, requirement=0.03, hm_days=14, comp=True):
        self.ticker = ticker  # ticker name being imported
        self.requirement = requirement  # if ticker price changes > than this then buy/sell/hold
        self.hm_days = hm_days  # how many days until threshold (requirement) is met?
        self.comp = comp      # compile TradeVol/AdjClose data (do if new data imported)

    # Join dfs for compile_data function
    def join_df(self, main_df=None, df=None, column=None):
        self.ticker = column.replace("_V/AP", "")
        if main_df.empty:
            main_df = abs(df)
        elif self.ticker in main_df:
            pass # no instruction if ticker column exists   
        else:
            main_df = main_df.join(abs(df), how='outer')
        return main_df
    
    
    # Create a CSV file out of ticker dataframe
    def compile_data(self, comp=True, picklepath='FTSE250.pickle', filename='file.csv'):
        # Get tickers
        with open(picklepath,'rb') as f:
            tickers = pickle.load(f)
        if comp:   
            # Empty Dataframe
            main_df = pd.DataFrame()
            price_df = pd.DataFrame()
            
            # Loop through tickers and append to csv
            for count, ticker in enumerate(tickers):
                df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
                df.set_index('Date', inplace=True)
                
                col_name ='{}_V/AP'.format(ticker)
                df[col_name] = df['Volume']/df['Adj Close']
                
                #Make a copy for dfp
                df_copy = df.copy(deep = True)
                df_copy.rename(columns = {'Adj Close': ticker}, inplace=True)
                
                # Drop excess columns (just date and col_name remain)
                df.drop(df.loc[:, df.columns != col_name].columns, 1, inplace=True)
                df_copy.drop(df_copy.loc[:, df_copy.columns != ticker].columns, 1, inplace=True)
        
                # Appending ticker dfs to main dfs 
                main_df = self.join_df(main_df=main_df, df=df, column=col_name)
                price_df = self.join_df(main_df=price_df, df=df_copy, column=ticker)
            
                if count % 25 == 0:
                    print('{} / {}'.format(count,len(tickers)))
            
            # Dropping Duplicated Rows in case
            #main_df = main_df.drop_duplicates(keep = False)
            #price_df = price_df.drop_duplicates(keep = False)
            
            # Turn Inf to 0
            main_df = main_df.replace([np.inf, -np.inf], 0)
            
            # Fill NaNs with 0
            main_df.fillna(0,inplace=True)
            price_df.fillna(0,inplace=True)
            
             # Replace All 0s with NaNs to stop skewing data
            #main_df = main_df.replace(0, np.nan)
            price_df = price_df.replace(0, np.nan)
    
            #Create CSV file
            main_df.to_csv(filename)
            price_df.to_csv('PricesDF.csv')
        else:
            main_df = pd.read_csv('VolPrice_DF.csv')
            main_df.set_index("Date", inplace=True)
            price_df = pd.read_csv('PricesDF.csv')
            price_df.set_index("Date", inplace=True)
        print('\nCOMPILED DATAFRAME:\n', main_df.head())
        return tickers, main_df, price_df
    
    
    # Extract Ticker data and apply hm_days shift
    def ticker_pct_change(self, main_df=None, ticker='GFS.L', hm_days=1):
        # Pull original csv file for ticker to get daily Adj Close prices
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        
        # Drop rows in ticker which contain zeros
        droplist = [main_df.index[i] for i, el in enumerate(main_df[ticker+'_V/AP']==0) if el == True]
        main_df = main_df.drop(droplist)
        for el in droplist:
            if el in df.index:
                df = df.drop(el)
    
        # Append all 1 to X days to dataframe in for loop
        n='Adj Close'
        for i in range(1, hm_days+1):
            # Determine percent change for 'hm_days' consecutive days
            main_df['{}_{}d'.format(ticker, i)] = (df[n].shift(-i)-df[n])/df[n]
        
        print('\nDATAFRAME WITH DAY SHIFT:\n', main_df.head())
        return main_df, droplist
    
    
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
    
    
    # Extract feature sets which will be passed to ML model
    def extract_featuresets(self, df, ticker, hm_days):
        # Collect dataframe with percent changes    
        df, droplist = self.ticker_pct_change(main_df=df, ticker=ticker, hm_days=hm_days)
    
        # map function passes 'x' columns of 'next day' data through the 
        # buy_sell_hold function. A 1, -1 or 0 is returned for each row
        # until the end and then this is turned into a list. Finally, 
        # this data is appended to the dataframe.
        complist = [df['{}_{}d'.format(ticker, i)] for i in range(1, hm_days+1)]
        df['{}_target'.format(ticker)] = list(map(self.buy_sell_hold,*complist))
        
        # Display buy/sell/hold split to user
        vals = df['{}_target'.format(ticker)].values.tolist()
        str_vals = [str(i) for i in vals]
        print('Data spread:', Counter(str_vals))
        
        # Take all the V/AP and calculate row by row percentage change
        tickers = df[df.columns[1:df.shape[1]-(hm_days+1)]]
        clean_df = df[[ticker for ticker in tickers]].pct_change()
        
        # Clean Data after percentage change
        clean_df = clean_df.replace([np.inf, -np.inf], 0) # Replace/ clean data again
        clean_df.fillna(0, inplace=True)
        
        print('[TRADE VOLUME/ADJUSTED CLOSE]%CHANGE/DAY\n',clean_df)
        
        # Replace All 0s with NaNs to stop skewing data
        #clean_df = clean_df.replace(0, np.nan)
        
        # X: feature sets, y: labels
        # X is all the normalised prices of the companies/ tickers
        # y is all the 1, -1 and 0 relationships for your dataframe
        X = clean_df.values
        y = df['{}_target'.format(ticker)].values
        return X, y, clean_df, droplist
    
    
    # Build a Classification ML model
    def do_ml(self, df, ticker=None, hm_days=1):
        X, y, clean_df, droplist = self.extract_featuresets(df, ticker, hm_days)
    
        # Keep dataset for final validation after ML
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        ids = np.array([np.where(np.all(X == i, axis=1))[0][0] for i in X_test])
        test_dates = np.array([clean_df.index[i] for i in ids])
        
        data = {'ids':  ids, 'test dates': test_dates}
        pltdat = pd.DataFrame (data, columns = ['ids', 'test dates'])
        pltdat.set_index('ids', inplace=True)
        pltdat = pltdat.sort_index()
        
        # Ensemble Voting Classifier
        clf = VotingClassifier([('knn', neighbors.KNeighborsClassifier(n_neighbors=5, n_jobs=-1)),
                                ('rfor', RandomForestClassifier(min_samples_leaf=150))])    
    
        # Fit Data (i.e. do the machine learning)
        clf.fit(X_train, y_train)
        
        # Check Accuracy of ML Model with K Folds Cross Validation
        scores = cross_val_score(clf, X, y, cv=10)
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        
        predictions = clf.predict(X_test)
        print('Prediction Spread: {}'.format(Counter(predictions)))
        
        # Store [TV/AC]%
        clean_df.to_csv('TV_AC_Dataframe.csv')
        
        #Store ML Model
        with open('{}_VAP_ML_model.pickle'.format(ticker), "wb") as f:
            pickle.dump(clf, f)
        return clf, scores.mean(), X, y, droplist, X_test, pltdat, clean_df
    

    def run_model(self):
        tickers, main_df, price_df = self.compile_data(comp=self.comp, filename='VolPrice_DF.csv')
        clf, acc, X, _, dp, X_test, pltdat, _ = self.do_ml(main_df, ticker=self.ticker, hm_days=self.hm_days)
        
        # Ticker Data
        price_df = price_df.drop(dp)
        prices = price_df[self.ticker]
        stockdates  = [datetime.strptime(d, "%Y-%m-%d").date() for d in price_df.index]
        
        try:
            preds = clf.predict(X)
            
            fig, ax1 = plt.subplots(1)
            
            #Plot overall ticker price
            ax1.plot_date(stockdates, prices, '-')
            for i, el in enumerate(preds):
                if i in pltdat.index:
                    if el ==1:
                        ax1.plot_date(stockdates[i], prices[i], 'go')
                    elif el == 0:
                        ax1.plot_date(stockdates[i], prices[i], 'ko')
                    else:
                        ax1.plot_date(stockdates[i], prices[i], 'ro')
        
            green_patch = mpatches.Patch(color='green', label='Buy')
            red_patch = mpatches.Patch(color='red', label='Sell')
            black_patch = mpatches.Patch(color='black', label='Hold')
            ax1.legend(handles=[green_patch, red_patch, black_patch])
            fig.suptitle('''
                         {} Machine Learning Classification Model
                         ML Model input data as: [Trade Volume / Adjusted Price]%change
                         DAY FORECAST: {},   %CHANGE THRESHOLD: {},   MODEL ACCURACY: {}
                         '''.format(self.ticker, self.hm_days, 100*self.requirement, round(acc,2)))
            ax1.set(xlabel='Date (day by day stock data)', ylabel='Adjusted Close Price (GBS)')
            fig.show()
        except:
            print(
            '''--> ERROR THROWN!
                Are Dimensions of ML model and input the same?
                If another company was added to the ticker list then
                this is likely the source of the error. Retrain Model
                to solve.
            ''')
            
# Run functions if this is the main script
if __name__ == '__main__':
    model = tickerML(ticker='FOUR.L', requirement=0.02, hm_days=10, comp=False)
    model.run_model()
