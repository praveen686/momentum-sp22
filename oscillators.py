#momentum oscillators for the input stock symbol over the input period 
class Oscillators(symbol, period):

    def getRelativeStrengthIndex(self, data):
        return self.RSI(symbol, period) 
    
    def getStochasticOscillator(self, data): 
        pass
    
    def getRateofChange(self, data): 
        pass
    
    def getMovingAverage(self, data):
        pass
    
    def getBollingerBands(self, data):
        pass
