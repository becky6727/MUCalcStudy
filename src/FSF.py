#comments
#ver1.0: prototype
#ver1.1: fitting function for 0th-order coefficient is changed.
#exponential is not so match, and then pol2 is introduced.
#ver2.0: any energy(RMW) can be used
#ver2.1: coefficients of fitting function are changed 
#whether the field size is over 20cm2 or not.

import sys, os
import numpy

class FSF:
    def __init__(self, Energy):
        self.Energy = Energy
        HOME = os.environ['HOME'] + '/work/Proton/EdgeScatter/'
        self.FilePar = '%s/src/par/Par_%s.table' %(HOME, Energy)
        self.ParArray = numpy.loadtxt(self.FilePar, unpack = True)
        
    def GetValue(self, FS, Nozzle):
        
        x = FS
        z = Nozzle
        
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
                
        return y
        
#end of class definition
