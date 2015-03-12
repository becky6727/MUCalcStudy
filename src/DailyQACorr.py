#comments
#ver.1.0: prototype

import os, sys
import datetime
import numpy
import scipy.interpolate

class DailyQACorr:
    def __init__(self, Energy):
        self.Energy = Energy
        HOME = os.environ['HOME'] + '/work/Proton/MUCalcStudy/'

        self.FileDQA = '%s/src/DailyQATable/OutputCorrTable_%s.table' %(HOME, Energy)
        
        #read file and set arrays
        f = open(self.FileDQA)
        
        self.DateArray = []
        self.OutputArray = []

        for line in f:
            L = line.strip()
            L = L.split(' ')

            #convert date -> timestamp
            tDate = datetime.datetime.strptime(L[0], '%Y-%m-%d')
            Date = datetime.date(tDate.year, tDate.month, tDate.day)
            Date = datetime.date.toordinal(Date)
    
            OutputF = float(L[1])/100.0
    
            self.DateArray.append(Date)
            self.OutputArray.append(OutputF)
        
            pass

        #convert data type
        self.DateArray = numpy.array(self.DateArray, dtype = float)
        self.OutputArray = numpy.array(self.OutputArray, dtype = float)
                   
        #interpolation with spline function
        self.Spl = scipy.interpolate.splrep(self.DateArray, self.OutputArray, s = 0)

    def GetValue(self, Date, Charge): #date is serial, not string!!
        
        x = Date
        Q = Charge
        
        DQCorr = scipy.interpolate.splev(x, self.Spl, der = 0)
        
        Qcorr = Q* (1.0 - DQCorr)
        
        return Qcorr
    
#end of class
