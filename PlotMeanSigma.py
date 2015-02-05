import os, sys, time
import numpy
import argparse
import ROOT

#options
Parser = argparse.ArgumentParser(description = 'options for plot')

Parser.add_argument('-p',
                    action = 'store_true',
                    dest = 'isPrint',
                    help = 'flag of printing the figure')

args = Parser.parse_args()

isPrint = args.isPrint

FileData = './Data/MeanSigma.dat'

if(not(os.path.exists(FileData))):
    print 'No such a file: %s' %(FileData)
    sys.exit()
    pass

#read data file
tmpArray = numpy.loadtxt(FileData, comments = '#', unpack = True)

EArray = [0 for i in range(len(tmpArray[0]))] #energy
ErrEArray = [0 for i in range(len(tmpArray[0]))] #dummy array
Mean1Array = [0 for i in range(len(tmpArray[0]))] #mean before correction
Mean2Array = [0 for i in range(len(tmpArray[0]))] #mean after correction
Sigma1Array = [0 for i in range(len(tmpArray[0]))] #sigma before correction
Sigma2Array = [0 for i in range(len(tmpArray[0]))] #sigma after correction

for i in range(len(EArray)):
    EArray[i] = tmpArray[0][i]
    ErrEArray[i] = 0.0
    
    Mean1Array[i] = tmpArray[1][i]
    Sigma1Array[i] = tmpArray[2][i]
    
    Mean2Array[i] = tmpArray[3][i]
    Sigma2Array[i] = tmpArray[4][i]
    pass

#convert data type
EArray = numpy.array(EArray)
ErrEArray = numpy.array(ErrEArray)
Mean1Array = numpy.array(Mean1Array)
Sigma1Array = numpy.array(Sigma1Array)
Mean2Array = numpy.array(Mean2Array)
Sigma2Array = numpy.array(Sigma2Array)

#draw plots
c1 = ROOT.TCanvas('c1', 'FSF', 0, 0, 800, 750)

c1.SetFillColor(0)
#c1.Divide(1, 2)
c1.SetGridx()
c1.SetGridy()
c1.Draw()

ROOT.gStyle.SetPalette(1)

MinE = 150.0
MaxE = 210.0

MinMean = -2.0
MaxMean = 2.0

gMeanSigma1 = ROOT.TGraphErrors(len(EArray), 
                                EArray, Mean1Array,
                                ErrEArray, Sigma1Array)

gMeanSigma2 = ROOT.TGraphErrors(len(EArray), 
                                EArray, Mean2Array,
                                ErrEArray, Sigma2Array)

gMeanSigma1.SetTitle('')
gMeanSigma1.GetXaxis().SetTitle('Energy [MeV]')
gMeanSigma1.GetXaxis().SetTitleFont(132)
gMeanSigma1.GetXaxis().SetTitleOffset(1.1)
gMeanSigma1.GetXaxis().SetTitleSize(0.045)
gMeanSigma1.GetXaxis().SetLabelFont(132)
gMeanSigma1.GetXaxis().SetLabelSize(0.04)
gMeanSigma1.GetXaxis().SetLimits(MinE, MaxE)
gMeanSigma1.GetYaxis().SetTitle('#Delta(dose/MU) [%]')
gMeanSigma1.GetYaxis().SetTitleFont(132)
gMeanSigma1.GetYaxis().SetTitleOffset(0.95)
gMeanSigma1.GetYaxis().SetTitleSize(0.045)
gMeanSigma1.GetYaxis().SetLabelFont(132)
gMeanSigma1.GetYaxis().SetLabelSize(0.04)
gMeanSigma1.SetMinimum(MinMean)
gMeanSigma1.SetMaximum(MaxMean)

gMeanSigma1.SetMarkerColor(2)
gMeanSigma1.SetMarkerStyle(8)
gMeanSigma1.SetMarkerSize(.9)
gMeanSigma1.SetLineWidth(2)
gMeanSigma1.SetLineColor(2)

gMeanSigma2.SetMarkerColor(4)
gMeanSigma2.SetMarkerStyle(8)
gMeanSigma2.SetMarkerSize(.9)
gMeanSigma2.SetLineWidth(2)
gMeanSigma2.SetLineColor(4)

gMeanSigma1.Draw('ap')
gMeanSigma2.Draw('psame')

#line @ zero
Lzero = ROOT.TLine(MinE, 0.0, MaxE, 0.0)

Lzero.SetLineColor(1)
Lzero.SetLineWidth(3)
Lzero.SetLineStyle(2)

Lzero.Draw('same')

#tolerance level
MinTole = -1.0
MaxTole = 1.0

ToleBox = ROOT.TBox(MinE, MinTole, MaxE, MaxTole)

ToleBox.SetFillColor(5)
ToleBox.SetFillStyle(3002)

ToleBox.Draw('same')
 
c1.Update()

#output
if(isPrint):
    GIF = './Figures/MeanSigma.gif'
    JPG = './Figures/MeanSigma.jpg'
    EPS = './Figures/EPS/MeanSigma.eps'
    
    c1.Print(GIF)
    c1.Print(JPG)
    c1.Print(EPS)
    
    pass

#end of program
