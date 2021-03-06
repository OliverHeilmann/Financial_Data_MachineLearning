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
    def __init__(self, tickerlist = None, taskno = None):
        self.tickerlist = tickerlist    # List of tickers
        self.taskno = str(taskno+1)     # String for printing in terminal
        self.trigger = False            # Indicate to user thread still functional
        self.ticker_prices = [None] * len(tickerlist)
        self.has_been_called=False
        self.terminationRequired = False
        Thread.__init__(self)
    
    # Stop thread from running
    def stop(self):
        self.terminationRequired = True
    
    # Pull ticker prices from thread
    def prices(self):
        return self.ticker_prices
    
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
       

# Thread to upload csv file to Github
class GithubUpdate(Thread):
    def __init__(self, filepath=None):
        self.trigger = False
        self.filepath = filepath
        self.terminationRequired = False
        Thread.__init__(self)
    
    def stop(self):
        self.terminationRequired = True
    
    # Upload .csv to github rep
    def upload_github(self):
        self.trigger = True

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


# Assign workers to tackle large ticker list
class AssignWorkers():
    # Stop all threads from running
    def stop_all(self):
        [workers['worker{}'.format(i)].stop() for i in range(0, len(workers))]
        print('Command to Stop Threads Passed...')
    
    # Pull tickerlist prices from all threads
    def pull_live_price(self):
        # Line below calls 'prices' function for each thread and stores into 
        # a final pricelist. Second for loop extracts the elements from the 
        # thread list.
        pricelist = [i for j in range(0,len(workers)) for i in workers['worker{}'.format(j)].prices()]
        pricelist.insert(0,datetime.now())
        # If any elements are None, return empty list to tell main script that
        # the threads are still collating ticker financial data.
        for i in pricelist:
            if i is None:
                pricelist = [None]
                break
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
                workers["worker" + str(task)] = LivePrice(tickerlist=workpack, taskno=task)
                workers["worker" + str(task)].start()

                first += division
                last += division

    
# Use for testing  
if __name__ == '__main__': 
    print('\nMAIN SCRIPT:\n')
    
    picklepath = 'FTSE250.pickle'
    if not os.path.exists(picklepath):
        print('\nNo path to ticker pickle...\n')
    else:
        with open(picklepath, "rb") as f:
            tickers = pickle.load(f)

        # Testing Github thread
        #    GH = GithubUpdate()
        #    GH.start()
        #    time.sleep(0.5)
        #    GH.upload_github()
        
        # Testing webscraping threads
        AW = AssignWorkers()
        AW.assignworkers(tickerlist=tickers, tickerNo = 100, workerNo = 5)
        time.sleep(5)
        for i in range(0,100):
            print(len(AW.pull_live_price()))
            time.sleep(2)
        AW.stop_all()