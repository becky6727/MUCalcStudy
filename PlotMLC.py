import os, sys, time
import numpy
import ROOT
import argparse
import scipy.interpolate
import src.MLC_Interpolation as MLC_Interp

#options
Parser = argparse.ArgumentParser(description = 'draw MLC structure')

Parser.add_argument('-i',
                    type = str,
                    default = None,
                    dest = 'Input',
                    help = 'Input File for plot MLC')

Parser.add_argument('-p',
                    action = 'store_true',
                    dest = 'isPrint',
                    help = 'flag of printing the result')

args = Parser.parse_args()

FileMLC = args.Input
isPrint = args.isPrint

#errors
if(FileMLC == None):
    print 'please choose input file to draw with option -i'
    sys.exit()
    pass

tmpArray = numpy.loadtxt(FileMLC, 
                         skiprows = 0, 
                         unpack = True)

#interplation of MLC structure
ObjMLC = MLC_Interp.MLC_Interpolation(tmpArray[0], tmpArray[1])
(AbsArray, ThetaArray) = ObjMLC.Interpolate()

#for MLC drawing
LeafArray = tmpArray[0] + 1j* tmpArray[1]

LeafEdge = numpy.min(numpy.real(LeafArray))

#draw canvas
c1 = ROOT.TCanvas('c1', 'MLC', 0, 0, 800, 750)

c1.SetFillColor(0)
c1.SetGridx()
c1.SetGridy()
#c1.Range(-70, -40, 70, 40)
c1.Draw()

ROOT.gStyle.SetPalette(1)

#draw axis
#MinX = numpy.min(numpy.real(LeafArray))
MinX = -127.0
MaxX = 127.0

MinY = -127.0
MaxY = 127.0

#fine structure
xArray = AbsArray* numpy.cos(ThetaArray)
yArray = AbsArray* numpy.sin(ThetaArray)

gMLC_fine = ROOT.TGraph(len(xArray), xArray, yArray)

gMLC_fine.SetTitle('MLC')
gMLC_fine.GetXaxis().SetTitle('')
gMLC_fine.GetXaxis().SetTitleFont(132)
gMLC_fine.GetXaxis().SetLabelFont(132)
gMLC_fine.GetXaxis().SetLimits(MinX, MaxX)
gMLC_fine.GetYaxis().SetTitle('')
gMLC_fine.GetYaxis().SetTitleFont(132)
gMLC_fine.GetYaxis().SetLabelFont(132)
gMLC_fine.SetMinimum(MinY)
gMLC_fine.SetMaximum(MaxY)

gMLC_fine.SetMarkerColor(2)
gMLC_fine.SetMarkerStyle(5)
gMLC_fine.SetMarkerSize(.9)
gMLC_fine.SetLineWidth(3)
gMLC_fine.SetLineColor(2)

gMLC_fine.Draw('apl')

#MLC drawn with lines
Lmlc = []

for i in range(len(LeafArray)):
    
    if(numpy.real(LeafArray[i]) > 0):
        Lobj = ROOT.TLine(numpy.real(LeafArray[i]), numpy.imag(LeafArray[i]), 
                          MaxX, numpy.imag(LeafArray[i]))
    else:
        #if(numpy.real(LeafArray[i]) != numpy.min(numpy.real(LeafArray))):
        if(numpy.real(LeafArray[i]) != MinX):
            Lobj = ROOT.TLine(numpy.real(LeafArray[i]), numpy.imag(LeafArray[i]), 
                              MinX, numpy.imag(LeafArray[i]))
        else:
            Lobj = ROOT.TLine(MinX, numpy.imag(LeafArray[i]), 
                              MaxX, numpy.imag(LeafArray[i]))
            pass
        
        pass
    
    Lobj.SetLineColor(4)
    Lobj.SetLineWidth(6)

    Lmlc.append(Lobj)

    pass

for i in range(len(Lmlc)):
    Lmlc[i].Draw('same')
    pass

#iso-center
Liso_X = ROOT.TLine(0.0, MinY, 0.0, MaxY)
Liso_Y = ROOT.TLine(MinX, 0.0, MaxX, 0.0)

Liso_X.SetLineColor(2)
Liso_X.SetLineWidth(3)
Liso_X.SetLineStyle(2)

Liso_Y.SetLineColor(2)
Liso_Y.SetLineWidth(3)
Liso_Y.SetLineStyle(2)

Liso_X.Draw()
Liso_Y.Draw()

c1.Update()
