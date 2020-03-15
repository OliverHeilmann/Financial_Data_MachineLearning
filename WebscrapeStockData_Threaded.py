"""
Created on Sat Mar 14 15:17:15 2020
@author: OliverHeilmann

This script webscrapes stock data using yahoo_fin. Number of threads can be 
defined (should be based on computer specs) and quantity of tickers to be 
scraped can also be selected. Main functions required are below: 
    AW = AssignWorkers()
    AW.assignworkers(tickerlist=tickers, tickerNo = X, workerNo = Y)
    AW.pull_live_price()
    AW.stop_all()   
"""
from threading import Thread
import pickle, os, math
from yahoo_fin import stock_info as si
from datetime import datetime
import time

# Thread to collect live stock data
class LivePrice(Thread):
    def __init__(self, tickerlist = None):
        self.tickerlist = tickerlist
        self.ticker_prices = []
        self.has_been_called=False
        self.terminationRequired = False
        Thread.__init__(self)
    
    # Stop thread from running
    def stop(self):
        self.terminationRequired = True
        print ("stopping")
    
    # Pull ticker prices from thread
    def prices(self):
        if self.ticker_prices == []:
            return [None]
        return self.ticker_prices
    
    # Thread will continually collect workpack finanical data
    def run(self):
        if not self.tickerlist == None:
            while not self.terminationRequired:
                # Get live price for tickers
                self.ticker_prices = [si.get_live_price(ticker) for ticker in self.tickerlist]
        else:
            print('No tickers passed...')
 

# Thread to upload csv file to Github
class GithubUpdate(Thread):
    def __init__(self):
        self.terminationRequired = False
        Thread.__init__(self)
    
    def stop(self):
        self.terminationRequired = True
        print ("stopping")
    
    # Upload .csv to github rep
    def upload_github(self):
        os.system("git status")
        time.sleep(1)
        os.system("git add .")
        time.sleep(3)
        os.system("git commit -m 'added'")
        time.sleep(3)
        os.system("git push")
        print('\nUPLOADED TO GITHUB\n')
    
    def run(self):
        while self.terminationRequired == False:
            print('No need to run Github thread...')
            time.sleep(0.01)
            pass
           

# Assign workers to tackle large ticker list
class AssignWorkers():
    # Stop all threads from running
    def stop_all(self):
        [workers['worker{}'.format(i)].stop() for i in range(0, len(workers))]
        print('Stopped all threads...')
    
    # Pull tickerlist prices from all threads
    def pull_live_price(self):
        # Line below calls 'prices' function for each thread and stores into 
        # a final pricelist. Second for loop extracts the elements from the 
        # thread list.
        pricelist = [i for j in range(0,len(workers)) for i in workers['worker{}'.format(j)].prices()]
        for i in pricelist:
            if i == None: 
                print('Wait for data to be collected...')
                return None
        pricelist.insert(0,datetime.now())
        return pricelist
    
    # Define number of tickers and threads to run
    def assignworkers(self, tickerlist=None, tickerNo = 5, workerNo = 1):
        global workers
        if not tickerlist == None:
            division = math.ceil(len(tickerlist[:tickerNo]) / workerNo)
            first = 0; last = division; workers = {}
            for task in range(0, workerNo):
                workpack = tickerlist[:tickerNo][first:last]
                
                # assign numbers to workers & start working
                workers["worker" + str(task)] = LivePrice(tickerlist=workpack)
                workers["worker" + str(task)].start()

                first += division
                last += division

    
# Use for testing  
if __name__ == '__main__': 
    print('MAIN SCRIPT:\n')
    
    picklepath = 'sp500tickers.pickle'
    if not os.path.exists(picklepath):
        print('\nNo path to ticker pickle...\n')
    else:
        with open(picklepath, "rb") as f:
            tickers = pickle.load(f)
    
#    GithubUpdate().upload_github()
#    AW = AssignWorkers()
#    AW.assignworkers(tickerlist=tickers, tickerNo = 100, workerNo = 5)
#    for i in range(0,10):
#        print(AW.pull_live_price())
#        time.sleep(2)
#    AW.stop_all()