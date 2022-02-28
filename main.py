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
        self.lookback = 252     # Momentum indicator lookback period
        self.num_coarse = 100   # Number of symbols selected at Coarse Selection
        self.num_fine = 50      # Number of symbols selected at Fine Selection

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
        pass

