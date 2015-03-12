import os, sys, time
import numpy
import ROOT
import argparse
import src.DailyQACorr as DQACorr

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

Parser.add_argument('-dqa',
                    action = 'store_true',
                    dest = 'isDQA',
                    help = 'flag of daily QA correction')

args = Parser.parse_args()

Energy = args.Energy
isPrint = args.isPrint
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
#DArray[4]: RS, cm
#DArray[5]: dose/MU, VQA
#DArray[6]: dose/MU, meas
#DArray[7]: dose/MU, Corrected

if(isDQA):    

    ObjDQA = DQACorr.DailyQACorr(Energy)

    for i in range(len(DArray[7])):
        DArray[6][i] = ObjDQA.GetValue(DArray[0][i], DArray[6][i])
        DArray[7][i] = ObjDQA.GetValue(DArray[0][i], DArray[7][i])
        pass
    
    pass

#difference between befor and after correction
dMUArray = 100.0* ((DArray[6] - DArray[5])/DArray[5])
dMUCorrArray = 100.0* ((DArray[6] - DArray[7])/DArray[7])

#data selection
FSArray = [0 for i in range(5)]
NozzleArray = [0 for i in range(5)]

FSArray[0] = numpy.array(DArray[1])
FSArray[1] = numpy.array(DArray[1][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                               (numpy.abs(dMUCorrArray) < 1.0))])
FSArray[2] = numpy.array(DArray[1][numpy.where((numpy.abs(dMUArray) > 1.0) &
                                               (numpy.abs(dMUCorrArray) < 1.0))])
FSArray[3] = numpy.array(DArray[1][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                               (numpy.abs(dMUCorrArray) > 1.0))])
FSArray[4] = numpy.array(DArray[1][numpy.where((numpy.abs(dMUArray) > 1.0) &
                                               (numpy.abs(dMUCorrArray) > 1.0))])

NozzleArray[0] = numpy.array(DArray[2])
NozzleArray[1] = numpy.array(DArray[2][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                                   (numpy.abs(dMUCorrArray) < 1.0))])
NozzleArray[2] = numpy.array(DArray[2][numpy.where((numpy.abs(dMUArray) > 1.0) &
                                                   (numpy.abs(dMUCorrArray) < 1.0))])
NozzleArray[3] = numpy.array(DArray[2][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                                   (numpy.abs(dMUCorrArray) > 1.0))])
NozzleArray[4] = numpy.array(DArray[2][numpy.where((numpy.abs(dMUArray) > 1.0) &
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
MaxFS = numpy.max(DArray[1]) + 5.0

MinNozzle = numpy.min(DArray[2]) - 5.0
MaxNozzle = numpy.max(DArray[2]) + 5.0

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

FSBin = 1.0
NBinFS = int((MaxFS - MinFS)/FSBin)

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

NozzleBin = 1.0
NBinNozzle = int((MaxNozzle - MinNozzle)/NozzleBin)

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
