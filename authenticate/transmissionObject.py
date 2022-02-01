#Transmission object to be used for translating test spectra to workable/storable data
class Transmission:
    #constructor expects an input of tVal list[str] and wVal list[str]
    def __init__(self, tVals, wVals):
        self.tVals = tVals
        self.wVals = wVals

    #returns a list[str] of each tVal
    def get_tVals(self):
        vals = []
        for i in range(len(self.tVals)) :
            vals.append(self.tVals[i])
        return vals

    #returns a list[str] of each wVal
    def get_wVals(self):
        vals = []
        for i in range(len(self.wVals)) :
            vals.append(self.wVals[i])
        return vals

    #sets the objects tVal list[str] to the input tVal list[str]
    def set_tVals(self, tVals):
        self.tVals = tVals

    #sets the objects wVal list[str] to the input wVal list[str]
    def set_wVals(self, wVals):
        self.wVals = wVals