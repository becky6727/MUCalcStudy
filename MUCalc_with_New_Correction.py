import os, sys, time
import numpy
import argparse
from openpyxl import load_workbook #read excel files
import src.FSF as FSFactor

#options
Parser = argparse.ArgumentParser(description = 'options for analysis')

Parser.add_argument('-E',
                    type = str,
                    dest = 'Energy',
                    default = 'S200',
                    help = 'Energy for analysis')

Parser.add_argument('-l',
                    type = str,
                    default = None,
                    dest = 'List',
                    help = 'List File Name')

args = Parser.parse_args()

Energy = args.Energy
List = args.List

#errors
if(List == None):
    print 'please type the list file name with option -l'
    sys.exit()
    pass

f = open(List)
FileExls = f.readlines()
f.close()

#data output
DArray = []

#object for calculating field size factor with field size and nozzle position
ObjFSF = FSFactor.FSF(Energy)

for i in range(len(FileExls)):
    
    File = FileExls[i].rstrip()
    
    wb = load_workbook(File, data_only = True)

    for j in range(12):
        
        #initialize
        tmpArray = [0 for i in range(5)]
        QA_ver = -1
        isPDD_Broken = False
        isPar_Broken = False
        
        ws = wb.worksheets[j]

        #is this QA sheet?
        if(str(ws.cell('L2').value) == 'None'):
            continue
        
        #has no contents
        if(ws.cell('B10').value == '#N/A'):
            continue
        
        #has no measured MU
        if(ws.cell('D49').value == '#DIV/0!'):
            continue

        #avoid example sheet
        if(str(ws.cell('B2').value) == 'None'):
            continue
        
        #QA sheet version check
        if(str(ws.cell('G48').value) == 'Gy'):
            QA_ver = 2
        elif(str(ws.cell('G48').value) == 'None'):
            QA_ver = 3
        else:
            QA_ver = -1
            pass
        
        if(QA_ver < 0):
            continue
        
        if((QA_ver == 2) and (ws.cell('D41').value == '#DIV/0!')):
            continue
        
        EnergyID = ws.cell('B7').value #energy
        FS = ws.cell('F56').value #mm
        Nozzle = ws.cell('B11').value #mm

        if(not(str(EnergyID) == Energy)):
            continue
        
        if(QA_ver != 3):
            
            dMU_Meas = (100.0* (ws.cell('D44').value))/(ws.cell('C46').value) 
            #measured dose ---> dose/MU
        
            #calc MU
            ROF = ws.cell('B29').value
            SOBPF = ws.cell('B30').value
            RSF = ws.cell('B31').value
            FSF = ws.cell('B32').value
            CSF = ws.cell('D41').value
            #PlanGy = ws.cell('D36').value
            PlanGy = ws.cell('C46').value
            
            if(str(PlanGy) == 'None'):
                isPar_Broken = True
                break
            
            #dMU_VQA = ROF* SOBPF* RSF* FSF* CSF #calc dose/MU
            dMU_VQA = ROF* SOBPF* RSF* FSF #calc dose/MU
        
        else:
                        
            dMU_Meas = (ws.cell('D47').value) #measured Gy --> dose/MU
            
            if(isinstance(dMU_Meas, unicode)):
                isPar_Broken = True
                break
            
            dMU_Meas = (100.0* dMU_Meas)/50.0
            
            #calc MU
            ROF = ws.cell('B29').value
            SOBPF = ws.cell('B30').value
            RSF = ws.cell('B31').value
            FSF = ws.cell('B32').value
            CSF = ws.cell('B33').value
            PlanGy = ws.cell('D36').value
                        
            if(str(PlanGy) == 'None'):
                isPar_Broken = True
                break
            
            #dMU_VQA = ROF* SOBPF* RSF* FSF* CSF #calc dose/MU
            dMU_VQA = ROF* SOBPF* RSF* FSF #calc dose/MU

            pass
        
        if(isPar_Broken):
            continue
        
        #calc modified d/MU with corrected FSF
        FS = FS/10.0 #mm -> cm
        FS = FS**2 #cm -> cm^{2}

        Nozzle = Nozzle/10.0 #mm -> cm
        Nozzle = Nozzle + 26.9 #distance from snout -> MLC-edge
        
        FSF_mod = ObjFSF.GetValue(FS, Nozzle)
        
        #dMU_mod = ROF* SOBPF* RSF* CSF* FSF_mod #modified calc dose/MU
        dMU_mod = ROF* SOBPF* RSF* FSF_mod #modified calc dose/MU
        
        tmpArray[0] = FS #cm^2
        tmpArray[1] = Nozzle #cm, distance from iso-center to MLC-edge
        tmpArray[2] = dMU_VQA
        tmpArray[3] = dMU_Meas
        tmpArray[4] = dMU_mod

        DArray.append(tmpArray)
        
        pass
    
    pass

#convert data type
DArray = numpy.array(DArray, dtype = float)

#output
Output = './Data/CorrectedMU_wo_CSF_%s.dat' %(Energy)

numpy.savetxt(Output, DArray, fmt = '%.4f', delimiter = ' ')
