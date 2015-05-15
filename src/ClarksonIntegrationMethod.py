#comments:
#ver1.0: prototype

#useage
#input parameters for initialization:
#Array of MLC(Real, Imaginary part), and Step of resolution of interpolation
#input parameters for calculating the Clarkson Integration
#Alpha(degree), dTheta(degree), Snout(cm), Energy(S200, S180,...)

import os, sys
import numpy
import MLC_Interpolation as MLC_Interp
import MLC_Evaluate as MLC_Eval
import FSF as FSFactor

class ClarksonIntegrationMethod:
    def __init__(self, Real, Imag, Step = 0.10):
        self.Real = Real
        self.Imag = Imag
                
        #set MLC structure
        ObjMLC = MLC_Interp.MLC_Interpolation(self.Real, self.Imag)
        
        self.Step = Step
        (rArray, ThetaArray) = ObjMLC.Interpolate(self.Step)
        
        #evaluate radius at specific angles
        self.ObjMLC_Eval = MLC_Eval.MLC_Evaluate(rArray, ThetaArray)

    def GetClarkson(self, Alpha, dTheta, Snout, Energy = None):
        
        if(Energy == None):
            print 'please choose the energy such as S200, S180,....'
            sys.exit()
            pass
        
        self.Energy = Energy
        self.Snout = Snout
        self.Alpha = Alpha
        self.dTheta = dTheta

        #degree -> radian
        self.Alpha = self.Alpha* (numpy.pi/180.0)
        self.dTheta = self.dTheta* (numpy.pi/180.0)
        
        AngleArray = numpy.arange(-numpy.pi + self.Alpha, 
                                   numpy.pi + self.Alpha + self.dTheta, 
                                   self.dTheta)

        ObjFSF = FSFactor.FSF(self.Energy)
        OptFSF = 'spl'
        
        S_total = 0.0
        
        for i in range(len(AngleArray)):
            
            Radius = self.ObjMLC_Eval.GetRadius(AngleArray[i])    
            Radius = numpy.sqrt(2)* (Radius/10.0) #mm -> cm
            
            FSF = ObjFSF.GetValue(Radius**2, self.Snout, OptFSF)
            
            S_total = S_total + FSF* (self.dTheta/(2.0* numpy.pi))
            
            pass
        
        return S_total

#end of class
