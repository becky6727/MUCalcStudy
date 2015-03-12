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
#DArray[0]: Field Size, cm^2
#DArray[1]: Nozzle position, cm
#DArray[2]: dose/MU, VQA
#DArray[3]: dose/MU, meas
#DArray[4]: dose/MU, Corrected

FSArray = numpy.array(DArray[1])
NozzleArray = numpy.array(DArray[2])
MUArray = numpy.array(DArray[6])
VQAMUArray = numpy.array(DArray[5])
CorrMUArray = numpy.array(DArray[7])

if(isDQA):    

    ObjDQA = DQACorr.DailyQACorr(Energy)

    for i in range(len(DArray[7])):
        DArray[6][i] = ObjDQA.GetValue(DArray[0][i], DArray[6][i])
        DArray[7][i] = ObjDQA.GetValue(DArray[0][i], DArray[7][i])
        pass
    
    pass

dMUArray = 100.0* ((DArray[6] - DArray[5])/DArray[5])
dMUCorrArray = 100.0* ((DArray[6] - DArray[7])/DArray[7])

#drow histgram
c1 = ROOT.TCanvas('c1', 'Edge Scattering', 0, 0, 800, 750)

c1.SetFillColor(0)
c1.Divide(1, 2)
#c1.SetGridx()
#c1.SetGridy()
c1.Draw()

ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)

#scatter plot(dose/MU)
Ncanvas = 1

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()

MinMU = 0.80
MaxMU = 1.50

gMU = ROOT.TGraph(len(MUArray), MUArray, VQAMUArray)
gMUCorr = ROOT.TGraph(len(MUArray), MUArray, CorrMUArray)

gMU.SetTitle('Scatter Plot for dose/MU')
gMU.GetXaxis().SetTitle('dose/MU, Measurement')
gMU.GetXaxis().SetTitleFont(132)
gMU.GetXaxis().SetTitleOffset(1.1)
gMU.GetXaxis().SetTitleSize(0.045)
gMU.GetXaxis().SetLabelFont(132)
gMU.GetXaxis().SetLabelSize(0.05)
gMU.GetXaxis().SetLimits(MinMU, MaxMU)
gMU.GetYaxis().SetTitle('dose/MU, Calculation')
gMU.GetYaxis().SetTitleFont(132)
gMU.GetYaxis().SetTitleOffset(0.80)
gMU.GetYaxis().SetTitleSize(0.045)
gMU.GetYaxis().SetLabelFont(132)
gMU.GetYaxis().SetLabelSize(0.05)
gMU.SetMinimum(MinMU)
gMU.SetMaximum(MaxMU)

gMU.SetMarkerColor(2)
gMU.SetMarkerStyle(5)
gMU.SetMarkerSize(.9)
gMU.SetLineWidth(3)
gMU.SetLineColor(2)

gMUCorr.SetMarkerColor(4)
gMUCorr.SetMarkerStyle(8)
gMUCorr.SetMarkerSize(.9)
gMUCorr.SetLineWidth(3)
gMUCorr.SetLineColor(4)

gMU.Draw('ap')
gMUCorr.Draw('psame')

#function of y = x
fyx = ROOT.TF1('fyx', '[0]* x', MinMU, MaxMU)

fyx.SetParameter(0, 1.0)

fyx.SetLineColor(1)
fyx.SetLineWidth(3)
fyx.SetLineStyle(2)

fyx.Draw('same')

#histogram
Ncanvas = 2

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()

MaxDiff = 4.0
MinDiff = -3.5
NBin = int((MaxDiff - MinDiff)/0.15)

h_dMU = ROOT.TH1F('h_dMU', 'dose/MU', NBin, MinDiff, MaxDiff)
h_dMUCorr = ROOT.TH1F('h_dMUCorr', 'dose/MU, modified', NBin, MinDiff, MaxDiff)

for i in range(len(dMUArray)):
    h_dMU.Fill(dMUArray[i])
    h_dMUCorr.Fill(dMUCorrArray[i])
    pass

h_dMU.GetXaxis().SetTitle('#Delta(dose/MU)[%]')
h_dMU.GetXaxis().SetTitleFont(132)
h_dMU.GetXaxis().SetTitleOffset(1.1)
h_dMU.GetXaxis().SetTitleSize(0.045)
h_dMU.GetXaxis().SetLabelFont(132)
h_dMU.GetXaxis().SetLabelSize(0.05)
h_dMU.GetYaxis().SetTitle('events/bin')
h_dMU.GetYaxis().SetTitleFont(132)
h_dMU.GetYaxis().SetTitleOffset(0.80)
h_dMU.GetYaxis().SetTitleSize(0.045)
h_dMU.GetYaxis().SetLabelFont(132)
h_dMU.GetYaxis().SetLabelSize(0.05)
h_dMU.SetMinimum(0.0)

if((h_dMU.GetMaximum() - h_dMUCorr.GetMaximum()) < 0.0):
    h_dMU.SetMaximum(1.10* (h_dMUCorr.GetMaximum()))
    pass

h_dMU.SetLineColor(2)
h_dMU.SetLineWidth(3)

h_dMUCorr.SetLineColor(4)
h_dMUCorr.SetLineWidth(3)
h_dMUCorr.SetFillStyle(3002)
h_dMUCorr.SetFillColor(4)

h_dMU.Draw()
h_dMUCorr.Draw('same')

#fitting
#MinFit = -0.8
#MaxFit = 2.0
MinFit = MinDiff
MaxFit = MaxDiff

fGaussFit = ROOT.TF1('fGaussFit', 'gaus', MinFit, MaxFit)

fGauss = ROOT.TF1('fGauss', 'gaus', MinDiff, MaxDiff)
fGaussCorr = ROOT.TF1('fGaussCorr', 'gaus', MinDiff, MaxDiff)

fGauss.SetLineColor(2)
fGauss.SetLineStyle(2)
fGauss.SetLineWidth(3)

fGaussCorr.SetLineColor(4)
fGaussCorr.SetLineStyle(2)
fGaussCorr.SetLineWidth(3)

for i in range(2):
    
    if(i != 0):
        Par0 = h_dMUCorr.GetMaximum()
        Par1 = h_dMUCorr.GetMean()
        Par2 = h_dMUCorr.GetRMS()
    else:
        Par0 = h_dMU.GetMaximum()
        Par1 = h_dMU.GetMean()
        Par2 = h_dMU.GetRMS()
        pass
    
    fGaussFit.SetParameter(0, Par0)
    fGaussFit.SetParameter(1, Par1)
    fGaussFit.SetParameter(2, Par2)
    
    if(i != 0):
        print 'fit histogram after modification'
        h_dMUCorr.Fit('fGaussFit', 'RL0')
            
        fGaussCorr.SetParameter(0, fGaussFit.GetParameter(0))
        fGaussCorr.SetParameter(1, fGaussFit.GetParameter(1))
        fGaussCorr.SetParameter(2, fGaussFit.GetParameter(2))
        
        LCorr = ROOT.TLine(fGaussFit.GetParameter(1), h_dMU.GetMinimum(),
                           fGaussFit.GetParameter(1), h_dMU.GetMaximum())
        
    else:
        print 'fit histogram before modification'
        h_dMU.Fit('fGaussFit', 'RL0')
                
        fGauss.SetParameter(0, fGaussFit.GetParameter(0))
        fGauss.SetParameter(1, fGaussFit.GetParameter(1))
        fGauss.SetParameter(2, fGaussFit.GetParameter(2))
        
        L = ROOT.TLine(fGaussFit.GetParameter(1), h_dMU.GetMinimum(),
                       fGaussFit.GetParameter(1), h_dMU.GetMaximum())
        
        pass
        
    pass

#set line profile
L.SetLineColor(2)
L.SetLineStyle(2)
L.SetLineWidth(3)

LCorr.SetLineColor(4)
LCorr.SetLineStyle(2)
LCorr.SetLineWidth(3)

fGauss.Draw('same')
fGaussCorr.Draw('same')

L.Draw('same')
LCorr.Draw('same')

c1.Update()

if(isPrint):
    GIF = './Figures/dMU_after_Modification_%s.gif' %(Energy)
    JPG = './Figures/dMU_after_Modification_%s.jpg' %(Energy)
    EPS = './Figures/EPS/dMU_after_Modification_%s.eps' %(Energy)
    
    c1.Print(GIF)
    c1.Print(JPG)
    c1.Print(EPS)
    
    pass

