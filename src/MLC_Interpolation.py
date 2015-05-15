#comments
#ver1.0: prototype

import sys, os
import numpy

class MLC_Interpolation:
    def __init__(self, Real, Imag):
        self.Real = Real
        self.Imag = Imag

        self.LeafArray = Real + 1j* Imag
        
    def Interpolate(self, Step = 0.10):
        LeafEdge = numpy.min(numpy.real(self.LeafArray))

        #leaf edge(upper, lower)
        EdgeNeg1 =  self.LeafArray[(numpy.real(self.LeafArray) > LeafEdge) & 
                                   (numpy.real(self.LeafArray) < 0.0) & 
                                   (numpy.imag(self.LeafArray) < 0.0)][-1]
        
        EdgeNeg2 = self.LeafArray[(numpy.real(self.LeafArray) > LeafEdge) & 
                                  (numpy.real(self.LeafArray) > 0.0) & 
                                  (numpy.imag(self.LeafArray) < 0.0)][0]
        
        EdgePos1 = self.LeafArray[(numpy.real(self.LeafArray) > LeafEdge) & 
                                  (numpy.real(self.LeafArray) > 0.0) & 
                                  (numpy.imag(self.LeafArray) > 0.0)][-1]

        EdgePos2 =  self.LeafArray[(numpy.real(self.LeafArray) > LeafEdge) & 
                                   (numpy.real(self.LeafArray) < 0.0) & 
                                   (numpy.imag(self.LeafArray) > 0.0)][0]

        #calc number of events at leaf edge position
        tmp = self.LeafArray[numpy.where(numpy.real(self.LeafArray) == numpy.min(numpy.real(self.LeafArray)))]
        NofNeg =  len(tmp[numpy.where(numpy.imag(tmp) < 0.0)])
        NofPos =  len(tmp[numpy.where(numpy.imag(tmp) > 0.0)])

        #interpolate leaf edge
        n = 0.0

        for i in range(len(self.LeafArray)):
            if(numpy.real(self.LeafArray[i]) == LeafEdge):
                n = n + 1.0
                if(numpy.imag(self.LeafArray[i]) <= 0.0):
                    self.LeafArray[i] = ((numpy.real(EdgeNeg1) + 
                                          ((numpy.real(EdgeNeg2) - numpy.real(EdgeNeg1))/NofNeg)*(n + 1.0))  + 
                                         1j* (numpy.imag(EdgeNeg1)))
                    pass
                pass
            pass

        n = 0.0

        for i in range(len(self.LeafArray)):
            if(numpy.real(self.LeafArray[i]) == LeafEdge):
                n = n + 1.0
                if(numpy.imag(self.LeafArray[i]) > 0.0):
                    self.LeafArray[i] = ((numpy.real(EdgePos1) - 
                                          ((numpy.real(EdgePos1) - numpy.real(EdgePos2))/NofPos)*(n + 1.0))  + 
                                         1j* (numpy.imag(EdgePos1)))
                    pass
                pass
            pass

        #linear interpolation
        VarArray = numpy.arange(0, len(self.LeafArray), 1)
        VarArraySpl = numpy.arange(0, len(self.LeafArray), Step)
        ThetaArraySpl = numpy.interp(VarArraySpl, VarArray, numpy.angle(self.LeafArray))
        AbsArraySpl = numpy.interp(VarArraySpl, VarArray, numpy.abs(self.LeafArray))

        return (AbsArraySpl, ThetaArraySpl)

#end of class
