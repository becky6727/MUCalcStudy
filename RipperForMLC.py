import os, sys, time
import numpy
import argparse

#options
Parser = argparse.ArgumentParser(description = 'ripping the MLC structure from info-tech file')

Parser.add_argument('-l',
                    type = str,
                    default = None,
                    dest = 'List',
                    help = 'List File Name')

args = Parser.parse_args()

List = args.List

#errors
if(List == None):
    print 'please type the list file name with option -l'
    sys.exit()
    pass

f = open(List)
FileCVS = f.readlines()
f.close()

for i in range(len(FileCVS)):
    
    File = FileCVS[i].rstrip()
    FileData = open(File)
    LineList = FileData.readlines()
    
    #MLC structrure array
    LeafLArray = []
    LeafRArray = []

    for Line in LineList:        
        tmp = Line.strip()
        array = tmp.split(',')
        
        if(array[0] == 'PatientID'):
            PatientID = str(array[1])
            continue
                
        if(array[0] == 'FieldName'):
            FieldID = str(array[1])
            continue

        if(array[0] == 'LeafNum'):
            LeafNum = int(array[1])
            continue
        
        if(len(array) < 3):
            continue
        
        LeafLArray.append(float(array[1]))
        LeafRArray.append(float(array[2]))
        
        if(array[0] == 'leaf1'):
            print 'end of MLC data'
            break
        
        pass

    LeafIDArray = numpy.arange(-(float(LeafNum-1)/2.0), 
                                float(LeafNum)/2.0, 1.0)
    LeafIDArray = 3.60* LeafIDArray #unit is mm
    LeafLArray = numpy.array(LeafLArray[::-1])
    LeafRArray = numpy.array(LeafRArray[::-1])

    #convert complex number to calc angle and radius easily
    tmpRArray = LeafRArray + 1j* LeafIDArray
    tmpLArray = LeafLArray + 1j* LeafIDArray
    
    tmp1Array = tmpLArray[numpy.where(numpy.angle(tmpLArray) < 0.0)]
    tmp2Array = tmpLArray[numpy.where(numpy.angle(tmpLArray) > 0.0)]
    
    rThetaArray = numpy.r_[tmp1Array[::-1], tmpRArray, tmp2Array[::-1]]
    
    #point at theta = pi/-pi
    Point = 0.5* (numpy.real(rThetaArray[0]) + numpy.real(rThetaArray[-1]))
    PointPi = Point + 1j* 1.0e-3
    Point_Pi = Point - 1j* 1.0e-3
        
    rThetaArray = numpy.r_[Point_Pi, rThetaArray, PointPi]
    
    Output = './Data/MLC_%s_%s.dat' %(PatientID, FieldID)
    
    numpy.savetxt(Output, 
                  numpy.transpose((numpy.real(rThetaArray), 
                                   numpy.imag(rThetaArray))),
                  fmt = '%2.5f %2.5f',
                  delimiter = ' ')
    pass

