import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from changefinder import cf
from scipy import stats
from math import floor
from datetime import timedelta
from collections import deque
import itertools as it
from decimal import Decimal

class ChangeFinderStart(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 8, 25)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.SetEndDate(2021, 8, 26)
        self.AddEquity("SPY", Resolution.Daily)
        
        tickers = [ 'XLK', 'QQQ', 'BANC', 'BBVA', 'BBD', 'BCH', 'BLX', 'BSBR', 'BSAC', 'SAN',
                    'CIB', 'BXS', 'BAC', 'BOH', 'BMO', 'BK', 'BNS', 'BKU', 'BBT','NBHC', 'OFG',
                    'BFR', 'CM', 'COF', 'C', 'VLY', 'WFC', 'WAL', 'WBK','RBS', 'SHG', 'STT', 'STL', 'SCNB', 'SMFG', 'STI']
                   
        self.symbols = []
        for i in tickers:
            self.symbols.append(self.AddEquity(i, Resolution.Daily).Symbol)
        
        self.formation_period = 252
        self.history_price = {}
        for symbol in self.symbols:
            hist = self.History([symbol], self.formation_period+1, Resolution.Daily)
            if hist.empty: 
                self.symbols.remove(symbol)
            else:
                self.history_price[str(symbol)] = deque(maxlen=self.formation_period)
                for tuple in hist.loc[str(symbol)].itertuples():
                    self.history_price[str(symbol)].append(float(tuple.close))
                if len(self.history_price[str(symbol)]) < self.formation_period:
                    self.symbols.remove(symbol)
                    self.history_price.pop(str(symbol))
        self.symbol_list = list(self.symbols) 
        
        

    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''
        
        for symbol in self.symbols:
            if data.Bars.ContainsKey(symbol) and str(symbol) in self.history_price:
                self.history_price[str(symbol)].append(float(data[symbol].Close)) 
        
        for symbol in self.symbol_list:
            #initialize changedfinder
            cf1 = cf.ChangeFinder (r = .01, order = 1, smooth = 8)
            if str(symbol) in self.history_price:
                arr = np.array(self.history_price[str(symbol)])
                mean = np.mean(arr)
                std = np.std(arr)
                for j in arr:
                    score = cf1.update(j)
                    
                #open position when CF score is above the mean (for now)
                if score[-1] > mean:
                    if not self.Portfolio[str(symbol)].Invested:
                        quantity = int(self.CalculateOrderQuantity(str(symbol), 0.2))
                        self.Buy(str(symbol), 100) 
                    elif self.Portfolio[str(symbol)].Invested:
                        self.Liquidate(str(symbol)) 
                     
            
            
