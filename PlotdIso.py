import os, sys, time
import numpy
import ROOT
import argparse

#parameter lists(Dose = Meas/VQA, GammaProx = Gamma-index@ProxUp)
ParList = ['PatientID', 'Energy[MeV]', 'SOBP[mm]', 'RS[mm]', 'Range[mm]', 
           'Snout[mm]', 'Angle[degree]', 'Depth[mm]', 
           'Iso Position[mm]', 'Distal Position[mm]', 'ProxUp Position[mm]', 
           'SOBP center Position[mm]', 'FS[mm]', 'Dose Diff.[%]', 'GammaProx',
           'dose/MU. measurement', 'Ratio = (dose/MU)_vqa/(dose/MU)_meas[%]',
           'SAD[mm]']

#options
Parser = argparse.ArgumentParser(description = 'options for plot')

Parser.add_argument('-ID',
                    action = 'store_true',
                    dest = 'isID',
                    help = 'falg of parameter for patient ID')

Parser.add_argument('-Energy',
                    action = 'store_true',
                    dest = 'isEnergy',
                    help = 'falg of parameter for Energy')

Parser.add_argument('-SOBP',
                    action = 'store_true',
                    dest = 'isSOBP',
                    help = 'falg of parameter for SOBP')

Parser.add_argument('-RS',
                    action = 'store_true',
                    dest = 'isRS',
                    help = 'falg of parameter for RS')

Parser.add_argument('-Range',
                    action = 'store_true',
                    dest = 'isRange',
                    help = 'falg of parameter for Range')

Parser.add_argument('-Snout',
                    action = 'store_true',
                    dest = 'isSnout',
                    help = 'falg of parameter for Snout')

Parser.add_argument('-Angle',
                    action = 'store_true',
                    dest = 'isAngle',
                    help = 'falg of parameter for Angle')

Parser.add_argument('-Depth',
                    action = 'store_true',
                    dest = 'isDepth',
                    help = 'falg of parameter for Depth')

Parser.add_argument('-iso',
                    action = 'store_true',
                    dest = 'isIso',
                    help = 'falg of parameter for Iso')

Parser.add_argument('-distal',
                    action = 'store_true',
                    dest = 'isDistal',
                    help = 'falg of parameter for Distal')

Parser.add_argument('-prox',
                    action = 'store_true',
                    dest = 'isProx',
                    help = 'falg of parameter for Prox')

Parser.add_argument('-CSOBP',
                    action = 'store_true',
                    dest = 'isCSOBP',
                    help = 'falg of parameter for SOBP center')

Parser.add_argument('-FS',
                    action = 'store_true',
                    dest = 'isFS',
                    help = 'falg of parameter for Field Size')

Parser.add_argument('-Dose',
                    action = 'store_true',
                    dest = 'isDose',
                    help = 'falg of parameter for Relative dose')

Parser.add_argument('-GammaProx',
                    action = 'store_true',
                    dest = 'isGammaProx',
                    help = 'falg of parameter for Gamma-index of ProxUp')

Parser.add_argument('-MU',
                    action = 'store_true',
                    dest = 'isMU',
                    help = 'falg of parameter for MU')

Parser.add_argument('-dMU',
                    action = 'store_true',
                    dest = 'isdMU',
                    help = 'falg of parameter for dMU')

Parser.add_argument('-SAD',
                    action = 'store_true',
                    dest = 'isSAD',
                    help = 'flag of parameter for SAD')

Parser.add_argument('-AnaDoseDiff',
                    action = 'store_true',
                    dest = 'isAnaDose',
                    help = 'flag of analyzing dose difference')

Parser.add_argument('-p',
                    action = 'store_true',
                    dest = 'isPrint',
                    help = 'flag of printing the figure')

args = Parser.parse_args()


ParFlag = [0 for i in range(18)]
 
ParFlag[0] = args.isID
ParFlag[1] = args.isEnergy
ParFlag[2] = args.isSOBP
ParFlag[3] = args.isRS
ParFlag[4] = args.isRange
ParFlag[5] = args.isSnout
ParFlag[6] = args.isAngle
ParFlag[7] = args.isDepth
ParFlag[8] = args.isIso
ParFlag[9] = args.isDistal
ParFlag[10] = args.isProx
ParFlag[11] = args.isCSOBP
ParFlag[12] = args.isFS
ParFlag[13] = args.isDose
ParFlag[14] = args.isGammaProx
ParFlag[15] = args.isMU
ParFlag[16] = args.isdMU
ParFlag[17] = args.isSAD
isAnaDose = args.isAnaDose
isPrint = args.isPrint

#errors
NofPar = 0

for i in range(len(ParFlag)):
    if(ParFlag[i]):
        NofPar += 1
        pass
    pass

if(NofPar != 1):
    print 'Please select "1" parameters for plotting the graph'
    print 'Parameters are as follows:'
    print ParList
    sys.exit()
    pass

#read data file
#FileData = './Data/EdgeScatterParameter.dat'
FileData = './Data/EdgeScatterParameter_20141120.dat'

if(not(os.path.exists(FileData))):
    print 'No such a file: %s' %(FileData)
    sys.exit()
    pass

tmpDataArray = numpy.loadtxt(FileData, skiprows = 0, unpack = True)

#perform data analysis
VQAMUArray = tmpDataArray[20]
MUArray = tmpDataArray[21]
dMUArray = 100.0* (1.0 - (VQAMUArray/MUArray))

RDoseArray = 100.0* (tmpDataArray[15]/tmpDataArray[13]) #(Prox dose)/(iso dose)
RDoseArray = 100.0* (1.0 - (tmpDataArray[18]/RDoseArray)) #1 - (VQA/Meas)

DataArray = []
YParArray = []
ParID = -1

for i in range(len(ParFlag)):
    if(i == 13):
        DataArray.append(RDoseArray)
    elif(i == 14):
        DataArray.append(100.0* tmpDataArray[19])
    elif(i == 15):
        DataArray.append(MUArray)
    elif(i == 16):
        DataArray.append(dMUArray)
    elif(i == 17):
        DataArray.append(tmpDataArray[22])
    else:
        DataArray.append(tmpDataArray[i])
        pass
    pass

for i in range(len(ParFlag)):
    if(ParFlag[i]):
        YParArray = DataArray[i]
        ParID = i
        pass
    pass

IsoArray = DataArray[8]
CSOBPArray = DataArray[11]

dIsoArray = CSOBPArray - IsoArray

#data convert
YParArray = numpy.array(YParArray, dtype = float)
dIsoArray = numpy.array(dIsoArray, dtype = float)

#data cut
if(not(isAnaDose)):
    XcutArray = dIsoArray[numpy.where((5.0 < RDoseArray) & (RDoseArray < 8.0))]
    YcutArray = YParArray[numpy.where((5.0 < RDoseArray) & (RDoseArray < 8.0))]
else:
    XcutArray = dIsoArray[numpy.where(numpy.abs(dMUArray) > 2.5)]
    YcutArray = YParArray[numpy.where(numpy.abs(dMUArray) > 2.5)]
    pass

#draw plots
c1 = ROOT.TCanvas('c1', 'Edge Scattering', 0, 0, 800, 750)

c1.SetFillColor(0)
#c1.Divide(1, 2)
c1.SetGridx()
c1.SetGridy()
c1.Draw()

ROOT.gStyle.SetPalette(1)

MinX = numpy.min(dIsoArray)
MaxX = numpy.max(dIsoArray)

MinY = numpy.min(YParArray)
MaxY = numpy.max(YParArray)

gPar = ROOT.TGraph(len(dIsoArray), dIsoArray, YParArray)
gParCut = ROOT.TGraph(len(XcutArray), XcutArray, YcutArray)

gPar.SetTitle('Difference between center of SOBP and iso-center : %s' 
              %(ParList[ParID]))
gPar.GetXaxis().SetTitle('Diff. between center of SOBP and iso-center [mm]')
gPar.GetXaxis().SetTitleFont(132)
gPar.GetXaxis().SetLabelFont(132)
gPar.GetXaxis().SetLimits(MinX, MaxX)
gPar.GetYaxis().SetTitle('%s' %(ParList[ParID]))
gPar.GetYaxis().SetTitleFont(132)
gPar.GetYaxis().SetLabelFont(132)
gPar.SetMinimum(MinY)
gPar.SetMaximum(MaxY)

gPar.SetMarkerColor(2)
gPar.SetMarkerStyle(8)
gPar.SetMarkerSize(.9)
gPar.SetLineWidth(3)
gPar.SetLineColor(2)

gParCut.SetMarkerColor(4)
gParCut.SetMarkerStyle(8)
gParCut.SetMarkerSize(.9)
gParCut.SetLineWidth(3)
gParCut.SetLineColor(4)

gPar.Draw('ap')
gParCut.Draw('psame')

c1.Update()

#Output of picture
if(isPrint):

    #EPS = './Figures/EdgeScatter_%s_%s.eps' %(ParList[ParID1], ParList[ParID2])
    GIF = './Figures/EdgeScatter_dIso_%s.gif' %(ParList[ParID])
    
    #c1.Print(EPS)
    c1.Print(GIF)
    
    pass

#end of program
