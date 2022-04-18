import numpy as np
import pandas as pd

from oscillators.py import Oscillators
from indicators.py import Indicators
from riskManager.py import RiskManager

class basicMomentum(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2009, 7, 1)  # Set Start Date
        self.SetEndDate(2019, 7, 1)    # Set Start Date       
        self.SetCash(100000)           # Set Strategy Cash

        self.UniverseSettings.Resolution = Resolution.Daily

        self.mom = {}           # Dict of Momentum indicator keyed by Symbol
        self.rsi = {}           # Dict of Relative Strength Index keyed by Symbol
        self.cci = {}           # Dict of Commodity Channel Index keyed by Symbol
        self.vol = {}           # using volume :)
        self.best = {}          # Dict to hold best stocks keyed by Symbol
        self.lookback = 252     # Momentum indicator lookback period
        self.num_coarse = 100   # Number of symbols selected at Coarse Selection
        self.num_fine = 50      # Number of symbols selected at Fine Selection
        self.num_long = 5       

        self.month = -1
        self.rebalance = False

        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)


    def CoarseSelectionFunction(self, coarse):  #Drop securities which have no fundamentals or too low prices.
        if self.month == self.Time.month:
            return Universe.Unchanged

        self.rebalance = True
        self.month = self.Time.month

        selected = sorted([x for x in coarse if x.HasFundamentalData and x.Price > 5],
            key=lambda x: x.DollarVolume, reverse=True)

        return [x.Symbol for x in selected[:self.num_coarse]]


    def FineSelectionFunction(self, fine):      #Select security with highest market cap
        
        fine = [f for f in fine if f.ValuationRatios.PERatio > 0
                               and f.EarningReports.BasicEPS.TwelveMonths > 0
                               and f.EarningReports.BasicAverageShares.ThreeMonths > 0]

        selected = sorted(fine,
            key=lambda f: f.ValuationRatios.PERatio *
                          f.EarningReports.BasicEPS.TwelveMonths *
                          f.EarningReports.BasicAverageShares.ThreeMonths,
            reverse=True)

        return [x.Symbol for x in selected[:self.num_fine]]

    def OnData(self, data):
        
        #  use multiple indicators
        #  make a weighted avg
        #  choose the top 5
        
        # Update the indicator
        
        for symbol, mom in self.mom.items():
            mom.Update(self.Time, self.Securities[symbol].Close)
        
        # manually updating the other indicators
        # for symbol, rsi in self.rsi.items():
        #     rsi.Update(self.Time, self.Securities[symbol].Close)
        # for symbol, cci in self.cci.items():
        #     cci.Update(self.Time, self.Securities[symbol].Close)
        # #
            
        if not self.rebalance:
            return

        # Sorts the stocks by three momentum indicators
        # sorted_mom = sorted([k for k,v in self.mom.items() if v.IsReady],
        #     key=lambda x: self.mom[x].Current.Value, reverse=True)
        # sorted_rsi = sorted([k for k,v in self.rsi.items() if v.IsReady],
        #     key=lambda x: self.rsi[x].Current.Value, reverse=True)
        # sorted_cci = sorted([k for k,v in self.cci.items() if v.IsReady],
        #     key=lambda x: self.cci[x].Current.Value, reverse=True)
        # sorted_vol = sorted([k for k,v in self.vol.items() if v.IsReady],
        #     key=lambda x: self.vol[x].Current.Value, reverse=True)

        #create weighted average
        # for symbol, mom in self.mom.items():
        #     best[symbol] = sorted_mom.index(symbol) + sorted_rsi.index(symbol) + sorted_cci.index(symbol)
            
        # other way of getting weighted avg
        for symbol, mom in self.mom.items():
            # best[symbol] = self.mom[symbol] + self.rsi[symbol] + self.cci[symbol] #add all the indicators together for that particular stock
            self.best[symbol] = self.mom[symbol].Current.Value + self.rsi[symbol].Current.Value + self.cci[symbol].Current.Value + self.vol[symbol].Current.Value
        #
        
        sorted_best = sorted([k for k,v in self.best.items()],
                    key=lambda x: self.best[x], reverse=True)
        selected = sorted_best[:self.num_long]

        # Liquidate securities that are not in the list
        for symbol, mom in self.mom.items():
            if symbol not in selected:
                if self.Securities[symbol].IsTradable and data.ContainsKey(symbol) and data[symbol] is not None:
                    self.Liquidate(symbol, 'Not selected')            
                
        # Buy selected securities
        for symbol in selected:
            if self.Securities[symbol].IsTradable and data.ContainsKey(symbol) and data[symbol] is not None:
                self.SetHoldings(symbol, 1/self.num_long)

        self.rebalance = False

    def OnSecuritiesChanged(self, changes):

             # Clean up data for removed securities and Liquidate
             for security in changes.RemovedSecurities:
                 symbol = security.Symbol
                 if self.mom.pop(symbol, None) is not None:
                     self.Liquidate(symbol, 'Removed from universe')

             for security in changes.AddedSecurities:
                 if security.Symbol not in self.mom:
                     self.mom[security.Symbol] = Momentum(self.lookback)
                 if security.Symbol not in self.rsi:
                     self.rsi[security.Symbol] = self.RSI(security.Symbol, self.lookback)
                 if security.Symbol not in self.cci:
                     self.cci[security.Symbol] = self.CCI(security.Symbol, self.lookback)
                 if security.Symbol not in self.vol:
                     self.vol[security.Symbol] = self.VWAP(security.Symbol, self.lookback)

             # Warm up the indicator with history price if it is not ready
             addedSymbols = [k for k,v in self.mom.items() if not v.IsReady]

             history = self.History(addedSymbols, 1 + self.lookback, Resolution.Daily)
             history = history.close.unstack(level=0)

             for symbol in addedSymbols:
                 ticker = str(symbol)
                 if ticker in history:
                     for time, value in history[ticker].items():
                         item = IndicatorDataPoint(symbol, time, value)
                         self.mom[symbol].Update(item)
                         self.rsi[symbol].Update(item)
                        #  self.vol[symbol].Update(item)
                        #  self.cci[symbol].Update(item)
