import os, sys, time
import numpy
import argparse
import ROOT

#options
Parser = argparse.ArgumentParser(description = 'options for plot')

Parser.add_argument('-E',
                    type = str,
                    dest = 'Energy',
                    default = 'S200',
                    help = 'Energy for plotting Field Size Factor')

Parser.add_argument('-Snout',
                    type = int,
                    dest = 'Snout',
                    default = '0',
                    help = 'Snout Position for plotting Field Size Factor')

Parser.add_argument('-p',
                    action = 'store_true',
                    dest = 'isPrint',
                    help = 'flag of printing the figure')

args = Parser.parse_args()

Energy = args.Energy
Snout = args.Snout
isPrint = args.isPrint

#errors
if(Energy == 'None'):
    print 'select energy: S200, S180, S160.... with option -E'
    sys.exit()
    pass

#SAD
if(Energy == 'S200'):
    SAD = 240.0 #cm
else:
    SAD = 0.0
    pass

if(Energy == 'S200'):
    SnoutArray = numpy.arange(5, 30, 5)
    SnoutArray = numpy.append(SnoutArray, 31)
else:
    SnoutArray = [0, 10]
    SnoutArray = numpy.array(SnoutArray)
    pass

FSArray = [0 for i in range(len(SnoutArray))]
FArray = [0 for i in range(len(SnoutArray))]
#FSArray = [0 for i in range(17)]
#FArray = [0 for i in range(17)]

if(Energy == 'S200'):
    FSnoutArray = [[] for i in range(9)]
else:
    #FSnoutArray = [[] for i in range(8)]
    FSnoutArray = [[] for i in range(17)]
    pass

RefFSArray = []

for i in range(len(SnoutArray)):
    
    FileFSF = './FSF/FSF_%s_Snout%d.table' %(Energy, int(SnoutArray[i]))
    
    if(not(os.path.exists(FileFSF))):
        continue
    
    (tmpFSArray, tmpFArray) = numpy.loadtxt(FileFSF, 
                                            comments = '#', 
                                            skiprows = 0, 
                                            unpack = True)
    
    FSArray[i] =  tmpFSArray  #cm^{2}
    #FSArray[i] =  numpy.sqrt(tmpFSArray) #cm
    FArray[i] = tmpFArray
    
    FSArray[i] = numpy.array(FSArray[i], dtype = float)
    FArray[i] = numpy.array(FArray[i], dtype = float)

    RefFSArray = FSArray[i]
    
    for j in range(len(RefFSArray)):
        
        if(len(numpy.where(FSArray[i] == RefFSArray[j])[0])):
            FSnoutArray[j].append(FArray[i][numpy.where(FSArray[i] == RefFSArray[j])][0])
        else:
            FSnoutArray[j].append(-1.0)
            pass
        pass
        
    pass

print FSnoutArray
FSnoutArray = numpy.array(FSnoutArray, dtype = float)
SnoutArray = (SnoutArray + 26.9)
#SnoutArray = numpy.float64(SnoutArray)
tmpSnoutArray = numpy.arange(5.0, 30.0, 5.0)
tmpSnoutArray = numpy.append(tmpSnoutArray, 31.0)

#draw plots
c1 = ROOT.TCanvas('c1', 'FSF', 0, 0, 800, 750)

c1.SetFillColor(0)
c1.Divide(1, 2)
#c1.SetGridx()
#c1.SetGridy()
c1.Draw()

ROOT.gStyle.SetPalette(1)

#Canvas1
Ncanvas = 1

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()
#c1.cd(Ncanvas).SetLogy()

MinFS = 0.0 #cm
MaxFS = 16.0 #cm

MinF = 0.99* numpy.min(FArray)
MaxF = 1.01* numpy.max(FArray)

gFSFArray = [0 for i in range(len(SnoutArray))]

for i in range(len(SnoutArray)):    
    
    gFSFArray[i] = ROOT.TGraph(len(FSArray[i]), FSArray[i], FArray[i])

    #gFSFArray[i].SetTitle('Field Size Factor: RMW = %s' %(Energy))
    gFSFArray[i].SetTitle('')
    #gFSFArray[i].GetXaxis().SetTitle('Field Size (cm^{2})')
    gFSFArray[i].GetXaxis().SetTitle('Length of a side of square field (cm)')
    gFSFArray[i].GetXaxis().SetTitleFont(132)
    gFSFArray[i].GetXaxis().SetTitleOffset(1.1)
    gFSFArray[i].GetXaxis().SetTitleSize(0.045)
    gFSFArray[i].GetXaxis().SetLabelFont(132)
    gFSFArray[i].GetXaxis().SetLabelSize(0.05)
    gFSFArray[i].GetXaxis().SetLimits(MinFS, MaxFS)
    gFSFArray[i].GetYaxis().SetTitle('Field Size Factor')
    gFSFArray[i].GetYaxis().SetTitleFont(132)
    gFSFArray[i].GetYaxis().SetTitleOffset(0.80)
    gFSFArray[i].GetYaxis().SetTitleSize(0.045)
    gFSFArray[i].GetYaxis().SetLabelFont(132)
    gFSFArray[i].GetYaxis().SetLabelSize(0.05)
    gFSFArray[i].SetMinimum(MinF)
    gFSFArray[i].SetMaximum(MaxF)
    
    gFSFArray[i].SetMarkerColor(i + 2)
    gFSFArray[i].SetMarkerStyle(i + 20)
    gFSFArray[i].SetMarkerSize(1.3)
    gFSFArray[i].SetLineWidth(2)
    gFSFArray[i].SetLineColor(i + 2)
    
    pass

gFSFArray[0].Draw('apl')

for i in range(len(SnoutArray) - 1):
    gFSFArray[i + 1].Draw('plsame')
    pass

#draw latex and markers
Latex = ROOT.TLatex()
Mark = ROOT.TMarker()

LatexFontSize = 0.075

for i in range(len(SnoutArray)):

    Xpos = 0.70* MaxFS
    Ypos = 0.93* MaxF - (0.012* i)

    Comment = 'Nozzle = %.1f cm' %(SnoutArray[i])

    Latex.SetTextSize(LatexFontSize)
    Latex.SetTextColor(i + 2)
    Latex.SetTextFont(132)
    
    Latex.DrawLatex(Xpos, Ypos, Comment)
    
    Mark.SetMarkerColor(i + 2)
    Mark.SetMarkerSize(1.3)
    Mark.SetMarkerStyle(i + 20)
        
    Mark.DrawMarker(0.97* Xpos, Ypos + 0.005)
    
    pass

#Canvas2
Ncanvas = 2

c1.cd(Ncanvas)
c1.cd(Ncanvas).SetGridx()
c1.cd(Ncanvas).SetGridy()
#c1.cd(Ncanvas).SetLogy()

MinSnout = 25.0
MaxSnout = 70.0

MinF = 0.99* numpy.min(FSnoutArray)
MaxF = 1.01* numpy.max(FSnoutArray)

gFSnoutArray = [0 for i in range(len(FSnoutArray))]
fFitArray = [0 for i in range(len(FSnoutArray))]

for i in range(len(FSnoutArray)):
    
    gFSnoutArray[i] = ROOT.TGraph(len(SnoutArray), SnoutArray, FSnoutArray[i])

    #gFSnoutArray[i].SetTitle('Field Size Factor as a function of Snout Position: RMW = %s' %(Energy))
    gFSnoutArray[i].SetTitle('')
    gFSnoutArray[i].GetXaxis().SetTitle('Nozzle Position (cm)')
    gFSnoutArray[i].GetXaxis().SetTitleFont(132)
    gFSnoutArray[i].GetXaxis().SetTitleOffset(1.1)
    gFSnoutArray[i].GetXaxis().SetTitleSize(0.045)
    gFSnoutArray[i].GetXaxis().SetLabelFont(132)
    gFSnoutArray[i].GetXaxis().SetLabelSize(0.05)
    gFSnoutArray[i].GetXaxis().SetLimits(MinSnout, MaxSnout)
    gFSnoutArray[i].GetYaxis().SetTitle('Field Size Factor')
    gFSnoutArray[i].GetYaxis().SetTitleFont(132)
    gFSnoutArray[i].GetYaxis().SetTitleOffset(0.80)
    gFSnoutArray[i].GetYaxis().SetTitleSize(0.045)
    gFSnoutArray[i].GetYaxis().SetLabelFont(132)
    gFSnoutArray[i].GetYaxis().SetLabelSize(0.05)
    gFSnoutArray[i].SetMinimum(MinF)
    gFSnoutArray[i].SetMaximum(MaxF)
    
    if(i < 8):
        gFSnoutArray[i].SetMarkerColor(i + 2)
        gFSnoutArray[i].SetLineColor(i + 2)
    else:
        gFSnoutArray[i].SetMarkerColor(i + 20)
        gFSnoutArray[i].SetLineColor(i + 20)
        pass
    
    gFSnoutArray[i].SetMarkerStyle(i + 20)
    gFSnoutArray[i].SetMarkerSize(1.2)
    gFSnoutArray[i].SetLineWidth(3)

    #define fitting function
    if(i < 5):
        fFitArray[i] = ROOT.TF1('f%d' %(i), 'pol1', MinSnout, MaxSnout)
    else:
        fFitArray[i] = ROOT.TF1('f%d' %(i), 'pol2', MinSnout, MaxSnout)
        pass
    
    if(i < 8):
        fFitArray[i].SetLineColor(i + 2)
    else:
        fFitArray[i].SetLineColor(i + 20)
        pass
    
    pass

gFSnoutArray[0].Draw('ap')
gFSnoutArray[0].Fit('f0', 'R0')

for i in range(len(gFSnoutArray)-1):
    gFSnoutArray[i + 1].Draw('psame')
    gFSnoutArray[i + 1].Fit('f%d' %(i + 1), 'R0+')
    pass

#draw latex
Latex2 = ROOT.TLatex()
Mark2 = ROOT.TMarker()

for i in range(len(RefFSArray)):

    Xpos = 0.88* MaxSnout
    Ypos = 0.97* MaxF - (0.012* i)

    Comment = 'FS = %d #times %d cm^{2}' %(RefFSArray[i], RefFSArray[i])
    
    if(i < 8):
        Latex2.SetTextColor(i + 2)
    else:
        Latex2.SetTextColor(i + 20)
        pass
    
    Latex2.SetTextSize(0.075)
    Latex2.SetTextFont(132)
    
    Latex2.DrawLatex(Xpos, Ypos, Comment)
    
    if(i < 8):
        Mark2.SetMarkerColor(i + 2)
    else:
        Mark2.SetMarkerColor(i + 20)
        pass
    
    Mark2.SetMarkerSize(1.3)
    Mark2.SetMarkerStyle(i + 20)
        
    Mark2.DrawMarker(0.98* Xpos, Ypos + 0.003)

    pass

c1.Update()

#Output of picture
if(isPrint):

    #EPS = './Figures/FSF_%s.eps' %(Energy)
    GIF = './Figures/FSF_%s.gif' %(Energy)
    
    #c1.Print(EPS)
    c1.Print(GIF)
    
    pass

#end of program
