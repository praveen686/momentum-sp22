import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from changefinder import cf

class ChangeFinderStart(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 8, 25)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.SetEndDate(2021, 8, 26)
        # self.AddEquity("SPY", Resolution.Minute)
        
        #Create a synthetic data set to test against
        points=np.concatenate([np.random.rand(100)+5,
                                         np.random.rand(100)+10,
                                         np.random.rand(100)+5])
        #CHANGEFINDER PACKAGE
        # Example 1
        f, (ax1, ax2) = plt.subplots(2, 1)
        f.subplots_adjust(hspace=0.4)
        ax1.plot(points)
        ax1.set_title("data point")
        #Initiate changefinder function
        cf1 = cf.ChangeFinder(order = 1, smooth = 7)
        scores = [cf1.update(p) for p in points]
        ax2.plot(scores)
        ax2.axhline(y=7)
        ax2.set_title("anomaly score")
        plt.show()
        
        # Example 2
        data = np.concatenate ([np.random.normal (0.7, 0.05, 300), 
        np.random.normal (1.5, 0.05 , 300), 
        np.random.normal (0.6, 0.05, 300), 
        np.random.normal (1.3, 0.05, 300)]) 
    
        cf2 = cf.ChangeFinder (r = .01, order = 1, smooth = 8)#r = .01, order = 1, smooth = 7) 
    
        ret1 = [] 
        for i in data: 
            score = cf2.update (i) 
            ret1.append (score) 
    
        fig = plt.figure () 
        ax3 = fig.add_subplot (111) 
        ax3.plot (ret1) 
        ax4 = ax3.twinx () 
        ax4 .plot (data,'r') 
        plt.show ()
    
        # Example 3
        # broken, current library does not have ARIMA implemented
        data2 = np.concatenate ([np.random.normal (0.7, 0.05, 300), 
        np.random.normal (1.5, 0.05 , 300), 
        np.random.normal (0.6, 0.05, 300), 
        np.random.normal (1.3, 0.05, 300)]) 
        arima_order = (1,0,0)
        cf3 = cf.ChangeFinderARIMA(term=30, smooth=7, order=arima_order)
    
        ret2 = [] 
        for i in data2: 
            score = cf3.update (i) 
            ret2.append (score) 
    
        fig2 = plt.figure () 
        ax5 = fig2.add_subplot (111) 
        ax5.plot (ret2) 
        ax6 = ax5.twinx () 
        ax6.plot (data2,'r') 
        plt.show ()
        


    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''

        # if not self.Portfolio.Invested:
        #    self.SetHoldings("SPY", 1)