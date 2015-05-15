import os, sys, time
import numpy, scipy.interpolate
import argparse
import ROOT

#options
Parser = argparse.ArgumentParser(description = 'options for plot')

Parser.add_argument('-E',
                    type = str,
                    dest = 'Energy',
                    default = 'S200',
                    help = 'Energy for plotting Field Size Factor')

Parser.add_argument('-p',
                    action = 'store_true',
                    dest = 'isPrint',
                    help = 'flag of printing the figure')

args = Parser.parse_args()

Energy = args.Energy
isPrint = args.isPrint

#errors
if(Energy == 'None'):
    print 'select energy: S200, S180, S160.... with option -E'
    sys.exit()
    pass

FilePar = './Data/FitParameters_%s.dat' %(Energy)

if(not(os.path.exists(FilePar))):
    print 'No such a file: %s' %(FilePar)
    sys.exit()
    pass

#field size array
if(Energy == 'S200'):
    FSArray = [15.0, 10.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0]
else:
    FSArray = [15.0, 10.0, 8.0, 6.0, 5.0, 4.0, 3.0, 2.0]
    pass

FSArray = [x**2 for x in FSArray]
FSArray = numpy.array(FSArray, dtype = float)
FSArray = FSArray[::-1]
FSArray = numpy.array(FSArray, dtype = float)
ErrFSArray = numpy.zeros(len(FSArray), dtype = float)

#read data file
tmpParArray = numpy.loadtxt(FilePar, 
                         comments = '#', 
                         skiprows = 0, 
                         unpack = True)

ParArray = [0 for i in range(3)]
ErrArray = [0 for i in range(3)]

for i in range(len(ParArray)):
    ParArray[i] = numpy.array(tmpParArray[2* i], dtype = float)
    ParArray[i] = ParArray[i][::-1]
    ParArray[i] = numpy.array(ParArray[i], dtype = float)
    ErrArray[i] = numpy.array(tmpParArray[2* i + 1], dtype = float)
    ErrArray[i] = ErrArray[i][::-1]
    ErrArray[i] = numpy.array(ErrArray[i], dtype = float)
    pass

#spline interpolation
FSStep = 1.0
FSArraySpl = numpy.arange(0.0, numpy.max(FSArray) + FSStep, FSStep)

ParArraySpl = [0 for i in range(3)]

for i in range(len(ParArraySpl)):
    Spl = scipy.interpolate.splrep(FSArray, ParArray[i], s = 0)
    ParArraySpl[i] = scipy.interpolate.splev(FSArraySpl, Spl, der = 0)
    pass

#set graphs
MinFS = 0.0
MaxFS = 230.0

gParArray = [0 for i in range(len(ParArray))]
gParSplArray = [0 for i in range(len(ParArraySpl))]

for i in range(len(gParArray)):
    
    MaxPar = 1.20* numpy.max(ParArray[i] + ErrArray[i])
    MinPar = numpy.min(ParArray[i] - ErrArray[i])
    
    if(MinPar < 0):
        MinPar = 1.20* MinPar
    else:
        MinPar = 0.80* MinPar
        pass
    
    gParArray[i] = ROOT.TGraphErrors(len(FSArray), FSArray, ParArray[i],
                                     ErrFSArray, ErrArray[i])
    
    gParSplArray[i] = ROOT.TGraph(len(FSArraySpl), FSArraySpl, ParArraySpl[i])

    gParArray[i].SetTitle('Parameter:%d-order' %(i))
    #gParArray[i].SetTitle('')
    gParArray[i].GetXaxis().SetTitle('Field Size (cm^{2})')
    gParArray[i].GetXaxis().SetTitleFont(132)
    gParArray[i].GetXaxis().SetTitleOffset(1.1)
    gParArray[i].GetXaxis().SetTitleSize(0.045)
    gParArray[i].GetXaxis().SetLabelFont(132)
    gParArray[i].GetXaxis().SetLabelSize(0.05)
    gParArray[i].GetXaxis().SetLimits(MinFS, MaxFS)
    gParArray[i].GetYaxis().SetTitle('Fiting Parameter')
    gParArray[i].GetYaxis().SetTitleFont(132)
    gParArray[i].GetYaxis().SetTitleOffset(0.80)
    gParArray[i].GetYaxis().SetTitleSize(0.045)
    gParArray[i].GetYaxis().SetLabelFont(132)
    gParArray[i].GetYaxis().SetLabelSize(0.05)
    gParArray[i].SetMinimum(MinPar)
    gParArray[i].SetMaximum(MaxPar)
    
    gParArray[i].SetMarkerColor(2)
    gParArray[i].SetMarkerStyle(i + 20)
    gParArray[i].SetMarkerSize(1.3)
    gParArray[i].SetLineWidth(2)
    gParArray[i].SetLineColor(2)

    gParSplArray[i].SetMarkerColor(4)
    gParSplArray[i].SetMarkerStyle(i + 20)
    gParSplArray[i].SetMarkerSize(1.3)
    gParSplArray[i].SetLineWidth(3)
    gParSplArray[i].SetLineStyle(2)
    gParSplArray[i].SetLineColor(4)

    pass

#draw plots
c1 = ROOT.TCanvas('c1', 'Fit Par', 0, 0, 800, 750)

c1.SetFillColor(0)
c1.Divide(2, 2)
#c1.SetGridx()
#c1.SetGridy()
c1.Draw()

ROOT.gStyle.SetPalette(1)

#Canvas1    
for i in range(len(ParArray)):

    Ncanvas = i + 1
    
    c1.cd(Ncanvas)
    c1.cd(Ncanvas).SetGridx()
    c1.cd(Ncanvas).SetGridy()

    gParArray[i].Draw('ap')
    gParSplArray[i].Draw('lsame')
        
    pass

c1.Update()
