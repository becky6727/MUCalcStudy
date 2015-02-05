import os, sys, time
import numpy
import ROOT
import argparse

#options
Parser = argparse.ArgumentParser(description = 'options for plot')

Parser.add_argument('-E',
                    type = str,
                    dest = 'Energy',
                    default = 'S200',
                    help = 'Energy for analysis')

Parser.add_argument('-p',
                    action = 'store_true',
                    dest = 'isPrint',
                    help = 'flag of printing the figure')

args = Parser.parse_args()

Energy = args.Energy
isPrint = args.isPrint

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

FSArray = numpy.array(DArray[0])
NozzleArray = numpy.array(DArray[1])
MUArray = numpy.array(DArray[3])
VQAMUArray = numpy.array(DArray[2])
CorrMUArray = numpy.array(DArray[4])

dMUArray = 100.0* ((DArray[3] - DArray[2])/DArray[2])
dMUCorrArray = 100.0* ((DArray[3] - DArray[4])/DArray[4])

#drow histgram
c1 = ROOT.TCanvas('c1', 'Edge Scattering', 0, 0, 800, 750)

c1.SetFillColor(0)
c1.Divide(2, 2)
#c1.SetGridx()
#c1.SetGridy()
c1.Draw()

ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)

#scatter plot(FS)
Ncanvas = 1

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()

MinFS = 0.0
MaxFS = 180.0

MinDiff = -4.0
MaxDiff = 4.0

gFS = ROOT.TGraph(len(FSArray), FSArray, dMUArray)
gFSCorr = ROOT.TGraph(len(FSArray), FSArray, dMUCorrArray)

gFS.SetTitle('Scatter Plot for dose/MU')
gFS.GetXaxis().SetTitle('Field Size [cm^{2}]')
gFS.GetXaxis().SetTitleFont(132)
gFS.GetXaxis().SetLabelFont(132)
gFS.GetXaxis().SetLimits(MinFS, MaxFS)
gFS.GetYaxis().SetTitle('#Delta(dose/MU)[%]')
gFS.GetYaxis().SetTitleFont(132)
gFS.GetYaxis().SetLabelFont(132)
gFS.SetMinimum(MinDiff)
gFS.SetMaximum(MaxDiff)

gFS.SetMarkerColor(2)
gFS.SetMarkerStyle(5)
gFS.SetMarkerSize(.9)
gFS.SetLineWidth(3)
gFS.SetLineColor(2)

gFSCorr.SetMarkerColor(4)
gFSCorr.SetMarkerStyle(8)
gFSCorr.SetMarkerSize(.9)
gFSCorr.SetLineWidth(3)
gFSCorr.SetLineColor(4)

gFS.Draw('ap')
gFSCorr.Draw('psame')

#scatter plot(Nozzle)
Ncanvas = 2

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()

MinNozzle = 25.0
MaxNozzle = 60.0

MinDiff = -4.0
MaxDiff = 4.0

gNozzle = ROOT.TGraph(len(NozzleArray), NozzleArray, dMUArray)
gNozzleCorr = ROOT.TGraph(len(NozzleArray), NozzleArray, dMUCorrArray)

gNozzle.SetTitle('Scatter Plot for dose/MU')
gNozzle.GetXaxis().SetTitle('Nozzle Position[cm]')
gNozzle.GetXaxis().SetTitleFont(132)
gNozzle.GetXaxis().SetLabelFont(132)
gNozzle.GetXaxis().SetLimits(MinNozzle, MaxNozzle)
gNozzle.GetYaxis().SetTitle('#Delta(dose/MU)[%]')
gNozzle.GetYaxis().SetTitleFont(132)
gNozzle.GetYaxis().SetLabelFont(132)
gNozzle.SetMinimum(MinDiff)
gNozzle.SetMaximum(MaxDiff)

gNozzle.SetMarkerColor(2)
gNozzle.SetMarkerStyle(5)
gNozzle.SetMarkerSize(.9)
gNozzle.SetLineWidth(3)
gNozzle.SetLineColor(2)

gNozzleCorr.SetMarkerColor(4)
gNozzleCorr.SetMarkerStyle(8)
gNozzleCorr.SetMarkerSize(.9)
gNozzleCorr.SetLineWidth(3)
gNozzleCorr.SetLineColor(4)

gNozzle.Draw('ap')
gNozzleCorr.Draw('psame')

#scatter plot(dose/MU)
Ncanvas = 3

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()

MinMU = -4.0
MaxMU = 4.0

gMU = ROOT.TGraph(len(dMUArray), dMUArray, dMUCorrArray)
#gMUCorr = ROOT.TGraph(len(MUArray), MUArray, CorrMUArray)

gMU.SetTitle('Scatter Plot for dose/MU')
gMU.GetXaxis().SetTitle('#Delta(dose/MU) before correction[%]')
gMU.GetXaxis().SetTitleFont(132)
gMU.GetXaxis().SetLabelFont(132)
gMU.GetXaxis().SetLimits(MinMU, MaxMU)
gMU.GetYaxis().SetTitle('#Delta(dose/MU) after correction[%]')
gMU.GetYaxis().SetTitleFont(132)
gMU.GetYaxis().SetLabelFont(132)
gMU.SetMinimum(MinMU)
gMU.SetMaximum(MaxMU)

gMU.SetMarkerColor(2)
gMU.SetMarkerStyle(5)
gMU.SetMarkerSize(.9)
gMU.SetLineWidth(3)
gMU.SetLineColor(2)

#gMUCorr.SetMarkerColor(4)
#gMUCorr.SetMarkerStyle(8)
#gMUCorr.SetMarkerSize(.9)
#gMUCorr.SetLineWidth(3)
#gMUCorr.SetLineColor(4)

gMU.Draw('ap')
#gMUCorr.Draw('psame')

#tolerance region
MinTol = -1.0
MaxTol = 1.0

L1 = ROOT.TLine(MinTol, MinMU, MinTol, MaxMU)
L2 = ROOT.TLine(MaxTol, MinMU, MaxTol, MaxMU)
L3 = ROOT.TLine(MinMU, MinTol, MaxMU, MinTol)
L4 = ROOT.TLine(MinMU, MaxTol, MaxMU, MaxTol)

L1.SetLineColor(4)
L1.SetLineStyle(2)
L1.SetLineWidth(3)

L2.SetLineColor(4)
L2.SetLineStyle(2)
L2.SetLineWidth(3)

L3.SetLineColor(4)
L3.SetLineStyle(2)
L3.SetLineWidth(3)

L4.SetLineColor(4)
L4.SetLineStyle(2)
L4.SetLineWidth(3)

L1.Draw('same')
L2.Draw('same')
L3.Draw('same')
L4.Draw('same')

c1.Update()
