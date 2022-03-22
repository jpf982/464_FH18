#!/usr/bin/env python
# coding: utf-8

import numpy as np
import collections as col
from copy import *
from database import db

# Compute the L^2 norm of two arrays, Tvals1 and Tvals2
# = C * \int_{\inf}^{\inf} \sqrt{(f_1(x)-f_2(x))^2} dx 
# set npoints = 0 for full L^2 norm, else set 
# npoints to number of random points to sample
def L2norm(npoints, Tvals1, Tvals2):

    # check, make sure arrays are same size
    #if(fvals1.size != fvals2.size or Tvals1.size != Tvals2.size):
    if(Tvals1.size != Tvals2.size):
        raise Exception("How did you get here? Check the size of your test and device spectra")
    nTvals = Tvals1.size
    if(npoints == 0): # use all points in spectra! We should do this by default
        dif = np.subtract(Tvals1,Tvals2)
        metric = (1/nTvals)*np.sqrt(np.sum(np.square(dif)))
    else: # approximate the norm
        intsum = 0
        for i in range(0, npoints):
            randIndex = np.random.randint(0, nTvals)
            intsum += (Tvals1[randIndex] - Tvals2[randIndex])^2
        metric = (1/npoints)*np.sqrt(intsum)
    return metric

class Authenticator: 
    
    # To use: Give correct inputs, and instantiate authenticator.
    # Then call auth.calculateMetrics, which will consider all of the devices and test spectra
    # Afterwards, call auth.authenticate to check on the best match, and accept/reject it.
    # returns PhQ ID string (success) or false (rejection)

    #Initialize authenticator with parameters:
    # Arbitrary metric cutoff (float) (0.05 for a test metricCutoff)
    # array of freq. vals from FTIR
    # array of T vals from FTIR
    # list of devices in DB
    # ID of the lock that the authenticator is running on ( make it anything atm "Kilimanjaro")
    def __init__(self, _metricCutoff, _testFreqvals, _testTvals, _lockID, dbase, _deviceDB=None):
        self.metricCutoff = _metricCutoff
        self.testFreqvals = deepcopy(_testFreqvals)
        self.testTvals = deepcopy(_testTvals)
        if(_deviceDB == None):
            _deviceDB == dbase.deviceList()
        self.deviceDB = _deviceDB # do not want a copy of the whole database! very silly. only ptrs
        self.lockID = _lockID
        # establish some facts about the test data
        self.npoints = np.size(_testFreqvals)
        self.maxfreq = np.amax(_testFreqvals)
        self.minfreq = np.amin(_testFreqvals)

    #default constructor with no parameters
    def __init__(self):
        """Default constructor of Authenticator object"""
        self.metricCutoff = 0.1
        self.testFreqvals = []
        self.testTvals = []
        self.deviceDB = None
        self.lockID = 0
        self.npoints = 0
        self.maxfreq = 100000.0
        self.minfreq = 0.0
    
    # Prime the authenticator, calculate matches
    # call with accuracy = 0 for full L^2 norm.
    # else call with n random points to estimate integral.
    def calculateMetrics(self, accuracy, keyList): # accuracy = how many sample points in spectra. 0 = ALL
        #DeviceScore = col.namedtuple('DeviceID_score', 'DeviceScore') #Line from above. Does it belong here?
        DeviceScore = col.namedtuple('DeviceScore', ['DeviceID', 'score']) #Line from above. Does it belong here?
        deviceScores = []
        print("Testing spectra with accuracy ", str(accuracy), " points. \n If npoints == 0, using full spectrum")
        print("Number of devices to test = ", len(self.deviceDB))
        for key in keyList: # loop over the devices and test them
    #        if(key.getPoints() != self.npoints or key.getMaxF() != self.maxfreq or key.getMinF() != self.minfreq):
    #           raise Exception("The test spectrum and device spectra are not on identical frequency grids. Fix this!")
            metric = L2norm(accuracy,self.testTvals,key.getTvals()) # perform test
            deviceScore = DeviceScore(deepcopy(key.getID()),metric) # make a named tuple, sort of like C struct
            deviceScores.append(deviceScore)
        self.DevicesAndScores = sorted(deviceScores, key=lambda x: x.score) # sort based on metric
        print("Authenticator is primed.")
        print(str(self.DevicesAndScores))
        return 

    # Finish the authentication
    # Return PhQ ID if successful, false if rejected
    def authenticate(self, dbase):
        try: 
            BestDevice = self.DevicesAndScores[0].DeviceID
        except NameError: 
                print("One must calculate the metrics first!")
                self.getMetrics(0) #need to initialize the metrics first!
                BestDevice = self.DevicesAndScores[0].DeviceID
        else: 
            metric = self.DevicesAndScores[0].score
        print("Best match: ", BestDevice)
        print("Norm of ", BestDevice, " and test spectrum = ", str(metric))
        print("With cutoff = ", self.metricCutoff)
        #acceptedKeys = dbase.keyList()
        #acceptKey = (BestDevice in acceptedKeys)
        acceptKey = True    #Hardcoding because there is only one "lock", i.e. the RasPi
        #print(str(acceptKey))
        if(metric < self.metricCutoff and acceptKey):
            print("Photonic Quasicrystal accepted!")
            return BestDevice
        else:
            if(metric >= self.metricCutoff): 
                print("Photonic Quasicrystal rejected! Not Recognized.")
            if(acceptKey != True):
                print("Photonic Quasicrystal rejected! Key not authorized.")
            return False

    #sets object attributes based on parameters
    def setValues(self, _metricCutoff, _testFreqvals, _testTvals, _lockID, _dbase):
        """Sets object attributes based on parameters
        
        Parameters
        ----------
        _metricCutoff : float
            new metricCutoff value
        _testFreqvals : list[float]
            new list of frequency values
        _testTvals : list[float]
            new list of t values
        _lockID : float
            new lockID value
        _dbase : database Object
            object that contains connection to the database
        """
        self.metricCutoff = _metricCutoff
        self.testFreqvals = deepcopy(_testFreqvals)
        self.testTvals = deepcopy(_testTvals)
        self.deviceDB = _dbase.deviceList()
        self.lockID = _lockID
        self.npoints = np.size(_testFreqvals)
        self.maxfreq = np.amax(_testFreqvals)
        self.minfreq = np.amin(_testFreqvals)
