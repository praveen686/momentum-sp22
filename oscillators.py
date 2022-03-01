#momentum oscillators for the input stock symbol over the input period 
class Oscillators(symbol, period):

    def getRelativeStrengthIndex(self, data):
        # do i also gotta specify the moving average or resolution type
        return self.RSI(symbol, period) 
    
    def getStochasticOscillator(self, data):
        # can also be return self.STO(symbol, period, kPeriod, dPeriod)
        return self.STO(symbol, period)
    
    def getRateofChange(self, data): 
        return self.ROC(symbol, period)
    
    def getMovingAverage(self, data, fastPeriod, slowPeriod, signalPeriod):
        return self.MACD(symbol, fastPeriod, slowPeriod, signalPeriod)
    
    def getBollingerBands(self, data, k, movingAverageType):
        return self.BB(symbol, period, k, movingAverageType)
