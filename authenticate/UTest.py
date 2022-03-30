import unittest 
import PhQ as phq
from database import db
import authenticate as auth
import testdriver as dr
import pandas as pd
import numpy as np

class testDriver(unittest.TestCase):

    #Returns True or False.
    #def test(self):
    #    self.assertTrue(True)

    #Check that what goes in the database is what comes out for small keys
    def test_smallKeys(self):
        print("test_smallKeys")
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
    def test_medKeys(self):
        print("test_medKeys")
        authenticator, dbase = dr.initialize()
        fVals = list(range(0,999))
        tVals = list(range(1,1000))
        names = ["med1", "med2", "med3", "med4", "med5"]
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

    #Check that what goes in the database is what comes out for large keys
    def test_bigKeys(self):
        print("test_bigKeys")
        authenticator, dbase = dr.initialize()
        fVals = list(range(0,4999))
        tVals = list(range(1,5000))
        names = ["big1", "big2", "big3", "big4", "big5"]
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

if __name__ == '__main__':
    unittest.main()