#comments
#ver1.0: prototype
#ver1.1: fitting function for 0th-order coefficient is changed.
#exponential is not so match, and then pol2 is introduced.
#ver2.0: any energy(RMW) can be used
#ver2.1: coefficients of fitting function are changed 
#whether the field size is over 20cm2 or not.

import sys, os
import numpy
import scipy.interpolate

class FSF:
    def __init__(self, Energy):
        self.Energy = Energy
        HOME = os.environ['HOME'] + '/work/Proton/MUCalcStudy/'
        
        self.FilePar = '%s/src/par/Par_%s.table' %(HOME, Energy)
        self.ParArray = numpy.loadtxt(self.FilePar, unpack = True)
        
        self.FileFitPar = '%s/src/par/FitParameters_%s.dat' %(HOME, Energy)
        self.FitParArray = numpy.loadtxt(self.FileFitPar, comments = '#', unpack = True)        
              
        #field size array
        if(Energy == 'S200'):
            self.FSArray = [15.0, 10.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0]
        else:
            self.FSArray = [15.0, 10.0, 8.0, 6.0, 5.0, 4.0, 3.0, 2.0]
            pass

    def GetValue(self, FS, Nozzle, Option = 'fit'):
        
        Opt = Option
        
        if(Opt != 'spl'):
            isOpt = False
        else:
            isOpt = True
            pass
        
        x = FS
        z = Nozzle

        if(not(isOpt)):
            
            if(x < 20.0):
                Coeff0 = (self.ParArray[0][0] + 
                          self.ParArray[1][0]* x + 
                          self.ParArray[2][0]* x**2)
                Coeff1 = (self.ParArray[0][1]* numpy.exp(self.ParArray[1][1]* x))
                Coeff2 = (self.ParArray[0][2]* numpy.exp(self.ParArray[1][2]* x))
            else:
                Coeff0 = (self.ParArray[3][0] + 
                          self.ParArray[4][0]* x + 
                          self.ParArray[5][0]* x**2)
                Coeff1 = (self.ParArray[2][1]* 
                          numpy.exp(self.ParArray[3][1]* (x - 20.0)))
                Coeff2 = 0.0
                pass
            
            #calc field size factor with field size and nozzle postion
            y = Coeff0 + Coeff1* z + Coeff2* z**2
        
        else:
            
            FSArray = [a**2 for a in self.FSArray]
            FSArray = numpy.array(FSArray, dtype = float)
            FSArray = FSArray[::-1]

            CoeffArray = [0 for i in range(3)]
            Coeff = [0 for i in range(3)]
            
            for i in range(len(CoeffArray)):
                CoeffArray[i] = numpy.array(self.FitParArray[2* i], dtype = float)
                CoeffArray[i] = CoeffArray[i][::-1]
                pass

            #spline interpolation
            FSStep = 0.10
            FSArraySpl = numpy.arange(0.0, numpy.max(FSArray) + FSStep, FSStep)
            
            ParArraySpl = [0 for i in range(3)]

            for i in range(len(ParArraySpl)):
                Spl = scipy.interpolate.splrep(FSArray, CoeffArray[i], s = 0)
                Coeff[i] = scipy.interpolate.splev(x, Spl, der = 0)
                pass
        
            y = Coeff[0] + Coeff[1]* z + Coeff[2]* z**2
            
            pass
        
        return y
        
#end of class definition
