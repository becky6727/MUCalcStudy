import os, sys, time
import numpy
import argparse
import src.DailyQACorr as DQACorr

#options
Parser = argparse.ArgumentParser(description = 'options for plot')

Parser.add_argument('-E',
                    type = str,
                    dest = 'Energy',
                    default = 'S200',
                    help = 'Energy for analysis')

Parser.add_argument('-dqa',
                    action = 'store_true',
                    dest = 'isDQA',
                    help = 'flag of daily QA correction')

args = Parser.parse_args()

Energy = args.Energy
isDQA = args.isDQA

#FileData = './Data/CorrectedMU_%s.dat' %(Energy)
#FileData = './Data/CorrectedMU_wo_CSF_%s.dat' %(Energy)
FileData = './Data/CorrectedMU_wo_CSF_%s_SPL.dat' %(Energy)

if(not(os.path.exists(FileData))):
    print 'No such a file: %s' %(FileData)
    sys.exit()
    pass

DArray = numpy.loadtxt(FileData, skiprows = 0, unpack = True)
#DArray[0]: Date, serial
#DArray[1]: Field Size, cm
#DArray[2]: Nozzle position, cm
#DArray[3]: SOBP, cm
#DArray[4]: RS, mm
#DArray[5]: dose/MU, VQA
#DArray[6]: dose/MU, meas
#DArray[7]: dose/MU, Corrected

#daily QA correction
if(isDQA):    

    ObjDQA = DQACorr.DailyQACorr(Energy)

    for i in range(len(DArray[7])):
        DArray[6][i] = ObjDQA.GetValue(DArray[0][i], DArray[6][i])
        DArray[7][i] = ObjDQA.GetValue(DArray[0][i], DArray[7][i])
        pass
    
    pass

dMUArray = 100.0* ((DArray[6] - DArray[5])/DArray[5])
dMUCorrArray = 100.0* ((DArray[6] - DArray[7])/DArray[7])

#calc total # of events
print '%s: Total Events = %d events' %(Energy, len(DArray[0]))

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

#end of program
