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

#difference between befor and after correction
dMUArray = 100.0* ((DArray[3] - DArray[2])/DArray[2])
dMUCorrArray = 100.0* ((DArray[3] - DArray[4])/DArray[4])

#data selection
FSArray = [0 for i in range(5)]
NozzleArray = [0 for i in range(5)]

FSArray[0] = numpy.array(DArray[0])
FSArray[1] = numpy.array(DArray[0][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                               (numpy.abs(dMUCorrArray) < 1.0))])
FSArray[2] = numpy.array(DArray[0][numpy.where((numpy.abs(dMUArray) > 1.0) &
                                               (numpy.abs(dMUCorrArray) < 1.0))])
FSArray[3] = numpy.array(DArray[0][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                               (numpy.abs(dMUCorrArray) > 1.0))])
FSArray[4] = numpy.array(DArray[0][numpy.where((numpy.abs(dMUArray) > 1.0) &
                                               (numpy.abs(dMUCorrArray) > 1.0))])

NozzleArray[0] = numpy.array(DArray[1])
NozzleArray[1] = numpy.array(DArray[1][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                                   (numpy.abs(dMUCorrArray) < 1.0))])
NozzleArray[2] = numpy.array(DArray[1][numpy.where((numpy.abs(dMUArray) > 1.0) &
                                                   (numpy.abs(dMUCorrArray) < 1.0))])
NozzleArray[3] = numpy.array(DArray[1][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                                   (numpy.abs(dMUCorrArray) > 1.0))])
NozzleArray[4] = numpy.array(DArray[1][numpy.where((numpy.abs(dMUArray) > 1.0) &
                                                   (numpy.abs(dMUCorrArray) > 1.0))])

#drow histgram
c1 = ROOT.TCanvas('c1', 'Edge Scattering', 0, 0, 800, 750)

c1.SetFillColor(0)
c1.Divide(2, 2)
#c1.SetGridx()
#c1.SetGridy()
c1.Draw()

ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)

#scatter plot
Ncanvas = 1

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()

MinFS = 0.0
MaxFS = numpy.max(DArray[0]) + 5.0

MinNozzle = 25.0
MaxNozzle = 60.0

gFSArray = [0 for i in range(len(FSArray))]

for i in range(len(gFSArray)):
    gFSArray[i] = ROOT.TGraph(len(FSArray[i]), FSArray[i], NozzleArray[i])

    gFSArray[i].SetTitle('Scatter Plot for dose/MU')
    gFSArray[i].GetXaxis().SetTitle('Field Size [cm^{2}]')
    gFSArray[i].GetXaxis().SetTitleFont(132)
    gFSArray[i].GetXaxis().SetLabelFont(132)
    gFSArray[i].GetXaxis().SetLimits(MinFS, MaxFS)
    gFSArray[i].GetYaxis().SetTitle('Nozzle Position')
    gFSArray[i].GetYaxis().SetTitleFont(132)
    gFSArray[i].GetYaxis().SetLabelFont(132)
    gFSArray[i].SetMinimum(MinNozzle)
    gFSArray[i].SetMaximum(MaxNozzle)
    
    gFSArray[i].SetMarkerColor(i + 2)
    gFSArray[i].SetMarkerStyle(8)
    gFSArray[i].SetMarkerSize(.9)
    gFSArray[i].SetLineWidth(3)
    gFSArray[i].SetLineColor(i + 2)
    
    pass

gFSArray[0].Draw('ap')

for i in range(len(gFSArray) - 1):
    gFSArray[i + 1].Draw('psame')
    pass

#histogram(field size)
Ncanvas = 2

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()

HistFSArray = [0 for i in range(len(FSArray))]

NBinFS = int((MaxFS - MinFS)/4.0)

for i in range(len(HistFSArray)):
    HistFSArray[i] = ROOT.TH1F('HistFS_%02d' %(i), 'hist of field size', NBinFS, MinFS, MaxFS)

    for j in range(len(FSArray[i])):
        HistFSArray[i].Fill(FSArray[i][j])
        pass

    HistFSArray[i].GetXaxis().SetTitle('Field Size [cm^{2}]')
    HistFSArray[i].GetXaxis().SetTitleFont(132)
    HistFSArray[i].GetXaxis().SetTitleOffset(1.1)
    HistFSArray[i].GetXaxis().SetTitleSize(0.045)
    HistFSArray[i].GetXaxis().SetLabelFont(132)
    HistFSArray[i].GetXaxis().SetLabelSize(0.05)
    HistFSArray[i].GetYaxis().SetTitle('events/bin')
    HistFSArray[i].GetYaxis().SetTitleFont(132)
    HistFSArray[i].GetYaxis().SetTitleOffset(0.80)
    HistFSArray[i].GetYaxis().SetTitleSize(0.045)
    HistFSArray[i].GetYaxis().SetLabelFont(132)
    HistFSArray[i].GetYaxis().SetLabelSize(0.05)    
    
    HistFSArray[i].SetLineColor(i + 2)
    HistFSArray[i].SetLineWidth(3)
    
    if(i != 0):
        HistFSArray[i].SetFillColor(i + 2)
        HistFSArray[i].SetFillStyle(3002)
        pass
    
    pass

HistFSArray[0].Draw()

for i in range(len(HistFSArray) - 1):
    HistFSArray[i + 1].Draw('same')
    pass

#histogram(Nozzle)
Ncanvas = 3

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()

HistNozzleArray = [0 for i in range(len(NozzleArray))]

NBinNozzle = int((MaxNozzle - MinNozzle)/2.0)

for i in range(len(HistNozzleArray)):
    HistNozzleArray[i] = ROOT.TH1F('HistNozzle_%02d' %(i), 'hist of Nozzle', 
                                   NBinNozzle, MinNozzle, MaxNozzle)

    for j in range(len(NozzleArray[i])):
        HistNozzleArray[i].Fill(NozzleArray[i][j])
        pass

    HistNozzleArray[i].GetXaxis().SetTitle('Nozzle Position [cm]')
    HistNozzleArray[i].GetXaxis().SetTitleFont(132)
    HistNozzleArray[i].GetXaxis().SetTitleOffset(1.1)
    HistNozzleArray[i].GetXaxis().SetTitleSize(0.045)
    HistNozzleArray[i].GetXaxis().SetLabelFont(132)
    HistNozzleArray[i].GetXaxis().SetLabelSize(0.05)
    HistNozzleArray[i].GetYaxis().SetTitle('events/bin')
    HistNozzleArray[i].GetYaxis().SetTitleFont(132)
    HistNozzleArray[i].GetYaxis().SetTitleOffset(0.80)
    HistNozzleArray[i].GetYaxis().SetTitleSize(0.045)
    HistNozzleArray[i].GetYaxis().SetLabelFont(132)
    HistNozzleArray[i].GetYaxis().SetLabelSize(0.05)    
    
    HistNozzleArray[i].SetLineColor(i + 2)
    HistNozzleArray[i].SetLineWidth(3)
    
    if(i != 0):
        HistNozzleArray[i].SetFillColor(i + 2)
        HistNozzleArray[i].SetFillStyle(3002)
        pass
    
    pass

HistNozzleArray[0].Draw()

for i in range(len(HistNozzleArray) - 1):
    HistNozzleArray[i + 1].Draw('same')
    pass

c1.Update()

#output
if(isPrint):
    GIF = './Figures/ProfileEventInOut_%s.gif' %(Energy)
    JPG = './Figures/ProfileEventInOut_%s.jpg' %(Energy)
    EPS = './Figures/EPS/ProfileEventInOut_%s.eps' %(Energy)
    
    c1.Print(GIF)
    c1.Print(JPG)
    c1.Print(EPS)

    pass

#end of program
