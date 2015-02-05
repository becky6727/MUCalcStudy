import os, sys, time
import numpy
import argparse
import ROOT

#options
Parser = argparse.ArgumentParser(description = 'options for plot')

Parser.add_argument('-E',
                    type = str,
                    dest = 'Energy',
                    default = 'None',
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
    ErrArray[i] = numpy.array(tmpParArray[2* i + 1], dtype = float)
    pass

#set graphs
MinFS = 0.0
MaxFS = 230.0

gParArray = [0 for i in range(len(ParArray))]

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

    pass

#fitting
fFitArray = [[0 for j in range(2)] for i in range(len(gParArray))]
fArray = [[0 for j in range(2)] for i in range(len(gParArray))]

MinFit1 = 0.0
MaxFit1 = 20.0

MinFit2 = 15.0
MaxFit2 = 225.0

for i in range(len(fFitArray)):

    if(i != 0):
        fFitArray[i][0] = ROOT.TF1('FitA_%d' %(i), 
                                   '[0]* exp([1]* x)', 
                                   #'pol2',
                                   MinFit1, MaxFit1)  
    else:
        fFitArray[i][0] = ROOT.TF1('FitA_%d' %(i), 
                                   #'[0]* exp([1]* x)', 
                                   'pol2',
                                   MinFit1, MaxFit1) 
        pass

    fFitArray[i][0].SetParameter(0, ParArray[i][-1])
    
    if(i != 0):
        fFitArray[i][1] = ROOT.TF1('FitB_%d' %(i), 
                                   '[0]* exp([1]* (x - 20.0))', 
                                   #'pol2', 
                                   MinFit2, MaxFit2)
    else:
        fFitArray[i][1] = ROOT.TF1('FitB_%d' %(i), 
                                   #'[0]* exp([1]* (x - 20.0))', 
                                   'pol2', 
                                   MinFit2, MaxFit2)
        pass
    
    fFitArray[i][1].SetParameter(0, ParArray[i][5])
    
    pass

#fitting
for i in range(len(ParArray)):
    
    gParArray[i].Fit('FitA_%d' %(i), 'R')
    
    if(i != 2):
        gParArray[i].Fit('FitB_%d' %(i), 'R+')    
        pass
    
    pass

#fitting with total function
FitParArray = [[0 for i in range(6)] for j in range(len(fFitArray[0]))]

for i in range(len(fFitArray[0])):
    for j in range(len(FitParArray)):
        FitParArray[j][2* i] = fFitArray[j][i].GetParameter(0)
        FitParArray[j][2* i + 1] = fFitArray[j][i].GetParameter(1)
        pass
    pass

fTotalArray = [0 for i in range(2)]

for i in range(len(fTotalArray)):

    if(i != 0):
        fTotalArray[i] = ROOT.TF1('fTotal_%d' %(i), 
                                  '[0]* exp([1]* x) + [2]* exp([3]* x)', 
                                  MinFS, MaxFS)
    else:
        fTotalArray[i] = ROOT.TF1('fTotal_%d' %(i), 
                                  'pol2(0) + pol2(3)', 
                                  MinFS, MaxFS)
        pass
    
    if(i != 0):
        for j in range(4):
            fTotalArray[i].SetParameter(j, FitParArray[i][j])
            pass
    else:
        for j in range(6):
            fTotalArray[i].SetParameter(j, FitParArray[i][j])
            pass
        pass
    
    fTotalArray[i].SetLineColor(1)
    fTotalArray[i].SetLineStyle(2)
    fTotalArray[i].SetLineWidth(3)
    
    gParArray[i].Fit('fTotal_%d' %(i), 'RQ0+')
        
    pass
    
#draw fitting function
for i in range(len(fArray)):
    
    fArray[i][0] = ROOT.TF1('exp%d', '[0]* exp([1]* x)', MinFS, MaxFS)
        
    if(i != 2):
        ParExp0 = fTotalArray[i].GetParameter(0)
        ParExp1 = fTotalArray[i].GetParameter(1)
    else:
        ParExp0 = fFitArray[i][0].GetParameter(0)
        ParExp1 = fFitArray[i][0].GetParameter(1)
        pass
    
    fArray[i][0].SetParameter(0, ParExp0)
    fArray[i][0].SetParameter(1, ParExp1)
        
    fArray[i][1] = ROOT.TF1('linear%d', '[0]* exp([1]* x)', MinFS, MaxFS)
        
    if(i != 2):
        ParLine0 = fTotalArray[i].GetParameter(2)
        ParLine1 = fTotalArray[i].GetParameter(3)
    else:
        ParLine0 = fFitArray[i][1].GetParameter(0)
        ParLine1 = fFitArray[i][1].GetParameter(1)
        pass
    
    fArray[i][1].SetParameter(0, ParLine0)
    fArray[i][1].SetParameter(1, ParLine1)
    
    #fArray[i][2] = ROOT.TF1('linear2%d', 'pol1', MinFS, MaxFS)
    
    #ParLine20 = fFitArray[i][2].GetParameter(0)
    #ParLine21 = fFitArray[i][2].GetParameter(1)
    #ParLine20 = fTotalArray[i].GetParameter(4)
    #ParLine21 = fTotalArray[i].GetParameter(5)
    
    #fArray[i][2].SetParameter(0, ParLine20)
    #fArray[i][2].SetParameter(1, ParLine21)
    
    for j in range(2):
        fArray[i][j].SetLineWidth(3)
        fArray[i][j].SetLineStyle(2)
        fArray[i][j].SetLineColor(j + 2)
        pass
    
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
    
    for j in range(2):
        #fArray[i][j].Draw('same')
        pass
    
    pass

c1.Update()
