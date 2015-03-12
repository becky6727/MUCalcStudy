#coding: utf-8
#generate excel sheet for the experiment of FSF measurement
#ver1.0

import os, sys, time
import numpy
import argparse
from openpyxl import Workbook #for writing excel files
from openpyxl.cell import get_column_letter

