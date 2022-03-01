#non-oscillator indicators 
class Indicators(symbol, period):
    def getChannelCommodityIndex(self, data):
        return self.CCI(symbol, period)
    
    def getSuperTrend(self, data, multiplier):
        return self.STR(symbol, period, multiplier)
    
    def getVolumeSpike(self, data):
        if(self.RDV(symbol, period) > 2):
            return self.RDV(symbol, period)
        else:
            return 1
    
    def getMoneyFlowIndex(self, data):
        return self.MFI(symbol, period)
    
    def getVWAP(self, data):
        return self.VWAP(symbol, period)

