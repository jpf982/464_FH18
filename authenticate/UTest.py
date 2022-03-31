import unittest 
import PhQ as phq
from database import db
import authenticate as auth
import testdriver as dr
import pandas as pd
import numpy as np

class testDriver(unittest.TestCase):

    #Check that what goes in the database is what comes out for small keys
    def smallKeys(self):
        print("\ntest_smallKeys", end=" ")
        authenticator, dbase = dr.initialize()
        fVals = list(range(0,299))
        tVals = list(range(1,300))
        dict = {'fVals': fVals, 'tVals': tVals}
        spectrum = pd.DataFrame(dict)
        names = ["small1", "small2", "small3", "small4", "small5"]
        for name in names:
            dr.insertSpectrum(dbase, spectrum, name)
        keyList = dr.getPhQ(dbase)
        for key in keyList:
            name, FVals, TVals = key.getValues()
            for i in range(len(FVals)):
                self.assertEqual(fVals[i],FVals[i])
                self.assertEqual(tVals[i],TVals[i])
        dbase.clearTable()
        dbase.exitDB()

    #Check that what goes in the database is what comes out for medium keys
    def medKeys(self):
        print("\ntest_medKeys", end=" ")
        authenticator, dbase = dr.initialize()
        fVals = list(range(0,999))
        tVals = list(range(1,1000))
        names = ["med1", "med2", "med3", "med4", "med5"]
        dict = {'fVals': fVals, 'tVals': tVals}
        spectrum = pd.DataFrame(dict)
        for name in names:
            dr.insertSpectrum(dbase, spectrum, name)
        keyList = dr.getPhQ(dbase)
        for key in keyList:
            name, FVals, TVals = key.getValues()
            for i in range(len(FVals)):
                self.assertEqual(fVals[i],FVals[i])
                self.assertEqual(tVals[i],TVals[i])
        dbase.clearTable()
        dbase.exitDB()

    #Check that what goes in the database is what comes out for large keys
    def bigKeys(self):
        print("\ntest_bigKeys", end=" ")
        authenticator, dbase = dr.initialize()
        fVals = list(range(0,4999))
        tVals = list(range(1,5000))
        names = ["big1", "big2", "big3", "big4", "big5"]
        dict = {'fVals': fVals, 'tVals': tVals}
        spectrum = pd.DataFrame(dict)
        for name in names:
            dr.insertSpectrum(dbase, spectrum, name)
        keyList = dr.getPhQ(dbase)
        for key in keyList:
            name, FVals, TVals = key.getValues()
            for i in range(len(FVals)):
                self.assertEqual(fVals[i],FVals[i])
                self.assertEqual(tVals[i],TVals[i])
        dbase.clearTable()
        dbase.exitDB()

    def diffKeys(self):
        print("\ntest_diffKeys", end=" ")
        authenticator, dbase = dr.initialize()
        fVals = list(range(0,4999))
        tVals = list(range(1,5000))
        name = "big"
        dict = {'fVals': fVals, 'tVals': tVals}
        spectrum = pd.DataFrame(dict)
        dr.insertSpectrum(dbase, spectrum, name)
        
        fVals = list(range(0,999))
        tVals = list(range(1,1000))
        name = "med"
        dict = {'fVals': fVals, 'tVals': tVals}
        spectrum = pd.DataFrame(dict)
        dr.insertSpectrum(dbase, spectrum, name)

        fVals = list(range(0,299))
        tVals = list(range(1,300))
        name = "med"
        dict = {'fVals': fVals, 'tVals': tVals}
        spectrum = pd.DataFrame(dict)
        dr.insertSpectrum(dbase, spectrum, name)

        keyList = dr.getPhQ(dbase)
        for key in keyList:
            name, FVals, TVals = key.getValues()
            for i in range(len(FVals)):
                self.assertEqual(fVals[i],FVals[i])
                self.assertEqual(tVals[i],TVals[i])
        dbase.clearTable()
        dbase.exitDB()

if __name__ == '__main__':
    unittest.main()