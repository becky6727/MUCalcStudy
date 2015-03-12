import os, sys, time
import numpy
import ROOT
import argparse

#options
Parser = argparse.ArgumentParser(description = 'options for plot')

Parser.add_argument('-p',
                    action = 'store_true',
                    dest = 'isPrint',
                    help = 'flag of printing the figure')

args = Parser.parse_args()

isPrint = args.isPrint

EneArray = ['S200', 'S160']
ParArray = [[0 for i in range(len(EneArray))] for j in range(6)]

for i in range(len(EneArray)):

    FileData = './src/par/Par_%s.table' %(EneArray[i])
    
    if(not(os.path.exists(FileData))):
        print 'No such a file: %s' %(FileData)
        continue
    
    tmpArray = numpy.loadtxt(FileData, comments = '#', unpack = True)
    
    for j in range(len(tmpArray)):
        for k in range(len(tmpArray[j])):
            ParArray[k][i] = tmpArray[j][k]
            pass
        pass
    
    pass

print ParArray
