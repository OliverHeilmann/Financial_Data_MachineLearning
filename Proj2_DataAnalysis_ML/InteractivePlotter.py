"""
Created on Tue Apr 14 23:32:58 2020

@author: OliverHeilmann
"""
import matplotlib.pyplot as plt
import numpy as np; np.random.seed(1)
from datetime import datetime
from sklearn import preprocessing
import pandas as pd
import pdb
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 20,10

# Clean input csv data. Yahoo Finance is fairly buggy and produces several 
# spurious results (negative prices, NaNs, zeros etc.). This function deletes 
# these companies where applicable.
def cleandata(df=None):
    # Some NaN values are ok -drop companies with excessive NaNs though
    nans = df.isna().sum(); droplist = ['Date']
    for company in df.columns[1:]:
        if nans[company]/df.shape[0] > 0.05:
            droplist.append(company)
#        else: 
#            # code below replaces '0' value with 'i-1' value to avoid returning
#            # 'inf' in the dmax equation.
#            for i, el in enumerate(df[company]):
#                if el <= 0 and i != len(df[company]):
#                    for I, El in enumerate(df[company][i:]):
#                        if El!=0:
#                            df[company][i] = df[company][i+I]
#                            break
#                elif i == len(df[company]):
#                    df[company][i] = df[company][i-1]
#                    
#            # If value percentage change is > 1000% it is probably false readings
#            # from Yahoo Finance. This is a known bug in the YF system. I have
#            # checked YF website and some companies have spurious/ false results 
#            # even in their plots. The code below identifies the gradient of each
#            # result and deletes companies with abnormally high changes in vals. 
#            # This is potentially dangerous so should be noted.
#            dmax = max(abs(np.diff(df[company]))/df[company].values[:-1])
#            if dmax > float(10):
#                pass
                #droplist.append(company)
    # Drop companies in droplist (from dataframe) and convert dataframe to 
    # numpy array for plotting below. PNL.L' is the personal asset trust.
    # NMC.L has folded and should therefore be exluded from results.
    df = df.drop(droplist, axis=1)
    
    # below is not a nice way to do this.... change later!
    try:
        df = df.drop(['DJAN.L','NMC.L'], axis=1)
    except:
        pass
    return df


# Plot this data on a heatmap (CORRELATION TABLE)
def visualize_corr_data(csv_name=None, companies=None, clean=True):
    df = pd.read_csv(csv_name)  
    
    # If companies defined, ignore others
    if companies != None:
        companies = ['Date'] + companies
        df = df[companies]
    
    # Clean dataframe data
    if clean:
        df = cleandata(df=df)
    else:
        df = df.drop('Date', axis=1)
    
    df = df[-100:]
    
    # Calculate correlation results
    df_corr = df.corr()
    print(df_corr.head())
    
    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    heatmap = ax.pcolor(data, cmap = plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    column_labels = df_corr.columns
    row_labels = df_corr.index
    
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.suptitle('Correlation Plot', fontsize=18)
    plt.show()
    return df_corr


# Plot the time series company data 
def time_series_plot(csv_name=None, Type=None, companies=None, clean=True, avg=True):  
    # Open Dataframe
    df = pd.read_csv(csv_name)
    
    for i in range(0,df.shape[0]):
        if df.loc[i].isna().sum() > int(df.shape[1]*0.01):
            df.drop([i])
    
     # Get Stock Dates for each row
    stockdates  = [datetime.strptime(d, "%Y-%m-%d").date() for d in df['Date']]
    
    # If companies defined, ignore others
    if companies != None:
        companies = ['Date'] + companies
        df = df[companies]
    
    # Clean dataframe data
    if clean:
        df = cleandata(df=df)
    else:
        df = df.drop('Date', axis=1)

    # User choice of plot type
    if Type=='Percentage Change':
        stockprices = df.pct_change().values
    elif Type=='Standardised':
        stockprices = df.values
        stockprices = preprocessing.StandardScaler().fit(stockprices[:][1:]).transform(stockprices.astype(float))
    elif Type=='Price':
        stockprices = df.values
    else:
        print('Pass Either:\n  Percentage Change\n  Standardised\n  Price')
    
    # Convert back to dataframe
    df = pd.DataFrame(data=stockprices, index=stockdates, columns=df.columns)
    
    # Add Average to plot if user specifies
    if avg:
        df['Average'] = df.sum(axis=1)/df.shape[1]
        stockprices = df.values

    # Make Figure
    fig1, ax1 = plt.subplots()
    
    # Make Annotation Function
    annot1 = ax1.annotate("", xy=(0,0), xytext=(20,20),
                          textcoords="offset points",
                          bbox=dict(boxstyle="round", fc="w"),
                          arrowprops=dict(arrowstyle="->"))
    annot1.set_visible(False)

    for company in df.columns:
        STKP = df[company].values
        if company == 'Average':
            # This is not particulary nice coding here, change later...
            newAvg = df[company].drop(df[company].index[np.where(df[company] == 0.0)[0]])
            ax1.plot(newAvg.index.values, newAvg.values, 'r-', linewidth=4, gid=company)
        else:
            ax1.plot(stockdates, STKP, '-',gid=company)

    def update_annot(ind,curve):
        index = ind["ind"][0]
        x = stockdates[index]
        y = stockprices[index][df.columns.get_loc(curve)]
        annot1.xy = [x, y]
        annot1.set_text(curve)
    
    def on_plot_hover(event):
        vis = annot1.get_visible()
        # Iterating over each data member plotted
        for curve in ax1.get_lines():
            cont, ind = curve.contains(event)
            if cont:
                update_annot(ind,curve.get_gid())
                annot1.set_visible(True)
                fig1.canvas.draw_idle()
            else:
                if vis:
                    annot1.set_visible(True)
                    fig1.canvas.draw_idle()
    
    fig1.canvas.mpl_connect('motion_notify_event', on_plot_hover) 
    ax1.set_xlabel('Date', fontsize=16)
    ax1.set_ylabel(Type, fontsize=16) 
    fig1.suptitle('{}'.format(csv_name), fontsize=18)
    if companies != None:
        ax1.legend(df.columns, loc="upper left")    
    fig1.show()