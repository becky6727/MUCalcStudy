#comments
#ver1.0: prototype

import os, sys
import numpy
import ROOT #for TGraph class

class MLC_Evaluate:
    def __init__(self, r, theta):
        self.rArray = r
        self.ThetaArray = theta
        
        #set TGraphPolar to evaluate theta
        self.gPolar = ROOT.TGraphPolar(len(self.rArray), 
                                       self.ThetaArray, 
                                       self.rArray)

    def GetRadius(self, angle = None):
        
        if(angle == None):
            print 'input angle is not valid'
            sys.exit()
            pass
        
        return self.gPolar.Eval(angle)

#end of class
