import os, sys, time
import numpy
import argparse

#options
Parser = argparse.ArgumentParser(description = 'options for plot')

Parser.add_argument('-E',
                    type = str,
                    dest = 'Energy',
                    default = 'S200',
                    help = 'Energy for analysis')

args = Parser.parse_args()

Energy = args.Energy

#FileData = './Data/CorrectedMU_%s.dat' %(Energy)
FileData = './Data/CorrectedMU_wo_CSF_%s.dat' %(Energy)

if(not(os.path.exists(FileData))):
    print 'No such a file: %s' %(FileData)
    sys.exit()
    pass

DArray = numpy.loadtxt(FileData, skiprows = 0, unpack = True)
#DArray[0]: Field Size, cm^2
#DArray[1]: Nozzle position, cm
#DArray[2]: dose/MU, VQA
#DArray[3]: dose/MU, meas
#DArray[4]: dose/MU, Corrected

dMUArray = 100.0* ((DArray[3] - DArray[2])/DArray[2])
dMUCorrArray = 100.0* ((DArray[3] - DArray[4])/DArray[4])

#calc total # of events
print 'Total Events = %d events' %(len(DArray[0]))

#calc within 1% diff. w/ or w/o modification
tmpArray = DArray[0][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                 (numpy.abs(dMUCorrArray) < 1.0))]

print 'within 1%% diff. w/ or w/o modification = %d events' %(len(tmpArray))

#calc within 1% w/ modification
tmpArray = DArray[0][numpy.where((numpy.abs(dMUCorrArray) < 1.0) &
                                 (numpy.abs(dMUArray) > 1.0))]

print 'within 1%% diff. w/ modification = %d events' %(len(tmpArray))

#calc within 1% w/o modification
tmpArray = DArray[0][numpy.where((numpy.abs(dMUCorrArray) > 1.0) &
                                 (numpy.abs(dMUArray) < 1.0))]

print 'within 1%% diff. w/o modification = %d events' %(len(tmpArray))

#calc out of 1% w/ or w/o modification
tmpArray = DArray[0][numpy.where((numpy.abs(dMUCorrArray) > 1.0) &
                                 (numpy.abs(dMUArray) > 1.0))]

print 'out of 1%% diff. w/ or w/o modification = %d events' %(len(tmpArray))
