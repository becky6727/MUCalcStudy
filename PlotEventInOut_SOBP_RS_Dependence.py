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
SOBPArray = [0 for i in range(5)]
RSArray = [0 for i in range(5)]

SOBPArray[0] = numpy.array(DArray[3])
SOBPArray[1] = numpy.array(DArray[3][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                               (numpy.abs(dMUCorrArray) < 1.0))])
SOBPArray[2] = numpy.array(DArray[3][numpy.where((numpy.abs(dMUArray) > 1.0) &
                                               (numpy.abs(dMUCorrArray) < 1.0))])
SOBPArray[3] = numpy.array(DArray[3][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                               (numpy.abs(dMUCorrArray) > 1.0))])
SOBPArray[4] = numpy.array(DArray[3][numpy.where((numpy.abs(dMUArray) > 1.0) &
                                               (numpy.abs(dMUCorrArray) > 1.0))])

RSArray[0] = numpy.array(DArray[4])
RSArray[1] = numpy.array(DArray[4][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                                   (numpy.abs(dMUCorrArray) < 1.0))])
RSArray[2] = numpy.array(DArray[4][numpy.where((numpy.abs(dMUArray) > 1.0) &
                                                   (numpy.abs(dMUCorrArray) < 1.0))])
RSArray[3] = numpy.array(DArray[4][numpy.where((numpy.abs(dMUArray) < 1.0) &
                                                   (numpy.abs(dMUCorrArray) > 1.0))])
RSArray[4] = numpy.array(DArray[4][numpy.where((numpy.abs(dMUArray) > 1.0) &
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

MinSOBP = 0.0
MaxSOBP = numpy.max(DArray[3]) + 5.0

MinRS = numpy.min(DArray[4]) - 5.0
MaxRS = numpy.max(DArray[4]) + 5.0

gSOBPArray = [0 for i in range(len(SOBPArray))]

for i in range(len(gSOBPArray)):
    gSOBPArray[i] = ROOT.TGraph(len(SOBPArray[i]), SOBPArray[i], RSArray[i])

    gSOBPArray[i].SetTitle('Scatter Plot for dose/MU')
    gSOBPArray[i].GetXaxis().SetTitle('SOBP [cm]')
    gSOBPArray[i].GetXaxis().SetTitleFont(132)
    gSOBPArray[i].GetXaxis().SetLabelFont(132)
    gSOBPArray[i].GetXaxis().SetLimits(MinSOBP, MaxSOBP)
    gSOBPArray[i].GetYaxis().SetTitle('Range Shifter [mm]')
    gSOBPArray[i].GetYaxis().SetTitleFont(132)
    gSOBPArray[i].GetYaxis().SetLabelFont(132)
    gSOBPArray[i].SetMinimum(MinRS)
    gSOBPArray[i].SetMaximum(MaxRS)
    
    gSOBPArray[i].SetMarkerColor(i + 2)
    gSOBPArray[i].SetMarkerStyle(8)
    gSOBPArray[i].SetMarkerSize(.9)
    gSOBPArray[i].SetLineWidth(3)
    gSOBPArray[i].SetLineColor(i + 2)
    
    pass

gSOBPArray[0].Draw('ap')

for i in range(len(gSOBPArray) - 1):
    gSOBPArray[i + 1].Draw('psame')
    pass

#histogram(field size)
Ncanvas = 2

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()

HistSOBPArray = [0 for i in range(len(SOBPArray))]

SOBPBin = 1.0
NBinSOBP = int((MaxSOBP - MinSOBP)/SOBPBin)

for i in range(len(HistSOBPArray)):
    HistSOBPArray[i] = ROOT.TH1F('HistSOBP_%02d' %(i), 'hist of SOBP', NBinSOBP, MinSOBP, MaxSOBP)

    for j in range(len(SOBPArray[i])):
        HistSOBPArray[i].Fill(SOBPArray[i][j])
        pass

    HistSOBPArray[i].GetXaxis().SetTitle('SOBP Width [cm]')
    HistSOBPArray[i].GetXaxis().SetTitleFont(132)
    HistSOBPArray[i].GetXaxis().SetTitleOffset(1.1)
    HistSOBPArray[i].GetXaxis().SetTitleSize(0.045)
    HistSOBPArray[i].GetXaxis().SetLabelFont(132)
    HistSOBPArray[i].GetXaxis().SetLabelSize(0.05)
    HistSOBPArray[i].GetYaxis().SetTitle('events/%.1f cm' %(SOBPBin))
    HistSOBPArray[i].GetYaxis().SetTitleFont(132)
    HistSOBPArray[i].GetYaxis().SetTitleOffset(0.80)
    HistSOBPArray[i].GetYaxis().SetTitleSize(0.045)
    HistSOBPArray[i].GetYaxis().SetLabelFont(132)
    HistSOBPArray[i].GetYaxis().SetLabelSize(0.05)    
    
    HistSOBPArray[i].SetLineColor(i + 2)
    HistSOBPArray[i].SetLineWidth(3)
    
    if(i != 0):
        HistSOBPArray[i].SetFillColor(i + 2)
        HistSOBPArray[i].SetFillStyle(3002)
        pass
    
    pass

HistSOBPArray[0].Draw()

for i in range(len(HistSOBPArray) - 1):
    HistSOBPArray[i + 1].Draw('same')
    pass

#histogram(RS)
Ncanvas = 3

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()

HistRSArray = [0 for i in range(len(RSArray))]

RSBin = 1.0
NBinRS = int((MaxRS - MinRS)/RSBin)

for i in range(len(HistRSArray)):
    HistRSArray[i] = ROOT.TH1F('HistRS_%02d' %(i), 'hist of RS', 
                                   NBinRS, MinRS, MaxRS)

    for j in range(len(RSArray[i])):
        HistRSArray[i].Fill(RSArray[i][j])
        pass

    HistRSArray[i].GetXaxis().SetTitle('RS [mm]')
    HistRSArray[i].GetXaxis().SetTitleFont(132)
    HistRSArray[i].GetXaxis().SetTitleOffset(1.1)
    HistRSArray[i].GetXaxis().SetTitleSize(0.045)
    HistRSArray[i].GetXaxis().SetLabelFont(132)
    HistRSArray[i].GetXaxis().SetLabelSize(0.05)
    HistRSArray[i].GetYaxis().SetTitle('events/%.1f mm' %(RSBin))
    HistRSArray[i].GetYaxis().SetTitleFont(132)
    HistRSArray[i].GetYaxis().SetTitleOffset(0.80)
    HistRSArray[i].GetYaxis().SetTitleSize(0.045)
    HistRSArray[i].GetYaxis().SetLabelFont(132)
    HistRSArray[i].GetYaxis().SetLabelSize(0.05)    
    
    HistRSArray[i].SetLineColor(i + 2)
    HistRSArray[i].SetLineWidth(3)
    
    if(i != 0):
        HistRSArray[i].SetFillColor(i + 2)
        HistRSArray[i].SetFillStyle(3002)
        pass
    
    pass

HistRSArray[0].Draw()

for i in range(len(HistRSArray) - 1):
    HistRSArray[i + 1].Draw('same')
    pass

#draw latex at canvas4
Ncanvas = 4
c1.cd(Ncanvas)

Latex = ROOT.TLatex()

for i in range(len(HistRSArray)):
    
    Xpos = 0.0
    Ypos = 0.7 - 0.1* i
    
    if(i == 0):
        Comment = 'Total Events: %d events' %(len(SOBPArray[0]))
    elif(i == 1):
        Comment = 'diff. < 1%% w/ or w/o new FSF: %d events' %(len(SOBPArray[1]))
    elif(i == 2):
        Comment = 'diff. < 1%% w/ new FSF: %d events' %(len(SOBPArray[2]))
    elif(i == 3):
        Comment = 'diff. < 1%% w/o new FSF: %d events' %(len(SOBPArray[3]))
    elif(i == 4):
        Comment = 'diff. > 1%% w/ or w/o new FSF: %d events' %(len(SOBPArray[4]))
        pass
    
    Latex.SetTextColor(i + 2)
    Latex.SetTextSize(0.065)
    Latex.SetTextFont(132)

    Latex.DrawLatex(Xpos, Ypos, Comment)

    pass

c1.Update()

#output
if(isPrint):
    GIF = './Figures/ProfileEventInOut_%s_SOBP_RS.gif' %(Energy)
    JPG = './Figures/ProfileEventInOut_%s_SOBP_RS.jpg' %(Energy)
    
    c1.Print(GIF)
    c1.Print(JPG)
    
    pass

#end of program
