#!/usr/bin/env python
# coding: utf-8

import numpy as np
from copy import *




#PhQ = namedtuple('PhQ', 'name identity Tvals freqvals npoints maxf minf')

# ugh I am conflicted if this should be a named tuple or object.
# I think object makes more sense + is more secure, I will explain on a call. 
# but my C/julia/haskell brain hates hates hates this

# NEVERMIND this is temporary, but needs to be handled as a namedtuple in the end
# before it is put in the database.

# name = anything
# ID = some hash function of the name
class PhQ:
    def __init__(self, _name, _identity, _freqvals, _Tvals):
        self.name = _name
        self.identity = _identity
        self.Tvals = deepcopy(_Tvals) #deepcopies for security reasons.
        self.freqvals = deepcopy(_freqvals)
        self.npoints = _freqvals.size
        self.maxf = np.amax(_freqvals)
        self.minf = np.amin(_freqvals)

    def setTvals(self, _Tvals):
        self.Tvals = _Tvals

    def setFreqvals(self, _freqvals):
        self.freqvals = _freqvals