#comments
#ver1.0: prototype, calculate chi2 from observed and expected values

import os, sys
import numpy

class ChiSquare:
    def __init__(self, obs, exp):
        self.obs = obs
        self.exp = exp
    
    def GetChiSquare(self):
        Obs = self.obs
        Exp = self.exp
        
        Chi2 = ((Obs - Exp)* (Obs - Exp))/Exp

        return Chi2

