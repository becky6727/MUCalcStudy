import os, sys, time
import numpy
import argparse
import src.ClarksonIntegrationMethod as ClarkInteg

#options
Parser = argparse.ArgumentParser(description = 'draw MLC structure')

Parser.add_argument('-i',
                    type = str,
                    default = None,
                    dest = 'Input',
                    help = 'Input File for plot MLC')

args = Parser.parse_args()

FileMLC = args.Input

#errors
if(FileMLC == None):
    print 'please choose input file to draw with option -i'
    sys.exit()
    pass

tmpArray = numpy.loadtxt(FileMLC, 
                         skiprows = 0, 
                         unpack = True)

#calc FSF with Clarkson Integration Method
Step = 0.10
ObjClarkson = ClarkInteg.ClarksonIntegrationMethod(tmpArray[0], 
                                                   tmpArray[1], 
                                                   Step)

#parameters for calc Clarkson Integration Method
Alpha = 0.0 #degree
dTheta = 10.0 #degree

#parameters for calc FSF
Snout = 5.0
Energy = 'S200'

S_total = ObjClarkson.GetClarkson(Alpha, dTheta, Snout, Energy)

print S_total
