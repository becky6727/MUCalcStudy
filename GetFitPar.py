import os, sys, time
import numpy
import argparse
import ROOT

#options
Parser = argparse.ArgumentParser(description = 'options')

Parser.add_argument('-E',
                    type = str,
                    dest = 'Energy',
                    default = 'None',
                    help = 'Energy for analyzing Field Size Factor')

args = Parser.parse_args()

Energy = args.Energy

#errors
if(Energy == 'None'):
    print 'select energy: S200, S180, S160.... with option -E'
    sys.exit()
    pass


if(Energy == 'S200'):
    SnoutArray = numpy.arange(5, 30, 5)
    SnoutArray = numpy.append(SnoutArray, 31)
else:
    SnoutArray = [0, 10, 20, 31]
    SnoutArray = numpy.array(SnoutArray)
    pass

FSArray = [0 for i in range(len(SnoutArray))]
FArray = [0 for i in range(len(SnoutArray))]

if(Energy == 'S200'):
    FSnoutArray = [[] for i in range(9)]
else:
    FSnoutArray = [[] for i in range(8)]
    pass

RefFSArray = []

for i in range(len(SnoutArray)):
    
    FileFSF = './FSF/FSF_%s_Snout%d.table' %(Energy, int(SnoutArray[i]))
    
    if(not(os.path.exists(FileFSF))):
        continue
    
    (tmpFSArray, tmpFArray) = numpy.loadtxt(FileFSF, 
                                            comments = '#', 
                                            skiprows = 0, 
                                            unpack = True)

    FSArray[i] =  tmpFSArray
    FArray[i] = tmpFArray
    
    FSArray[i] = numpy.array(FSArray[i], dtype = float)
    FArray[i] = numpy.array(FArray[i], dtype = float)

    RefFSArray = FSArray[0]
    
    for j in range(len(RefFSArray)):
        
        if(len(numpy.where(FSArray[i] == RefFSArray[j])[0])):
            FSnoutArray[j].append(FArray[i][numpy.where(FSArray[i] == RefFSArray[j])][0])
        else:
            FSnoutArray[j].append(-1.0)
            pass
        pass
        
    pass

FSnoutArray = numpy.array(FSnoutArray, dtype = float)
SnoutArray = (SnoutArray + 26.9)

MinSnout = 25.0
MaxSnout = 70.0

MinF = 0.99* numpy.min(FSnoutArray)
MaxF = 1.01* numpy.max(FSnoutArray)

gFSnoutArray = [0 for i in range(len(FSnoutArray))]
fFitArray = [0 for i in range(len(FSnoutArray))]

for i in range(len(FSnoutArray)):
    
    gFSnoutArray[i] = ROOT.TGraph(len(SnoutArray), SnoutArray, FSnoutArray[i])

    gFSnoutArray[i].GetXaxis().SetLimits(MinSnout, MaxSnout)
    gFSnoutArray[i].SetMinimum(MinF)
    gFSnoutArray[i].SetMaximum(MaxF)
    
    #define fitting function
    if(RefFSArray[i] > 20.0):
        fFitArray[i] = ROOT.TF1('f%d' %(i), 'pol1', MinSnout, MaxSnout)
    else:
        fFitArray[i] = ROOT.TF1('f%d' %(i), 'pol2', MinSnout, MaxSnout)
        pass
    
    pass

ParArray = [[0 for i in range(6)] for j in range(len(gFSnoutArray))]

for i in range(len(FSnoutArray)):
    gFSnoutArray[i].Fit('f%d' %(i), 'RQ0')
    
    for j in range(3):
        ParArray[i][2*j] = fFitArray[i].GetParameter(j)
        ParArray[i][2*j + 1] = fFitArray[i].GetParError(j)
        pass
    
    pass

#convert data type
ParArray = numpy.array(ParArray, dtype = float)

#output
header = 'Format is as follows:(Par1) (Err1) (Par2) (Err2) ....'
Output = './Data/FitParameters_%s.dat' %(Energy)

numpy.savetxt(Output, (ParArray), 
              fmt = '%.3e',
              header = header, 
              delimiter = ' ')

#end of program
