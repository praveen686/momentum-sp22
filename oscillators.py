#momentum oscillators for the input stock symbol over the input period 
class Oscillators(symbol, period):

    def getRelativeStrengthIndex(self, data):
        # do i also gotta specify the moving average or resolution type
        return self.RSI(symbol, period) 
    
    def getStochasticOscillator(self, data): 
        pass
    
    def getRateofChange(self, data): 
        return self.ROC(symbol, period)
    
    def getMovingAverage(self, data):
        return self.MACD(symbol, fastPeriod, slowPeriod, signalPeriod)
    
    def getBollingerBands(self, data):
        pass
