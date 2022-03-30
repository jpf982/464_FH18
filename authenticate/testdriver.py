import PhQ as phq
from database import db
import authenticate as auth

#Drive the authentication process through this file
def initialize() :
    """Initially create and return authenticator and database objects"""
    authenticator = auth.Authenticator()
    dbase = db.database()
    return authenticator, dbase

#function to use the database object to create and return a pandas
# dataframe of the tVals and fVals of the spectrum at the location 
# specified by path parameter
def getSpectrum(dbase, path) :
    """Read in list of freqVals and tVals and return as a dataframe
    
    Parameters
    ----------
    dbase : database Object
        object that contains the actual connection to the database
    path : str
        string of the filepath to the FTIR spectrum
    """
    spectrum = dbase.readFile(path)
    print("Got spectrum.")
    return spectrum

#function to insert the spectrum values as a PhQ object into the database
def insertSpectrum(dbase, spectrum, keyName) :
    """Create a PhQ Object with the spectrum values and give that to the database
    
    Parameters
    ----------
    dbase : database Object
        object that contains the actual connection to the database
    spectrum : pandas.dataframe
        dataframe of the tVals and fVals
    keyName : str
        user input name of the key
    """
    #Check for duplicates!!!! 
    key = phq.PhQ(keyName, spectrum['fVals'], spectrum['tVals'])
    return dbase.insert(key)

#function to check the key for values outside 0 and 1
def preprocessKey() :
    """Check the key for values outside 0 and 1"""
    return True

#function to set the values in the authenticator object
def setVals(spectrum, authenticator, dbase) :
    """Set the values in the authenticator object

    Parameters
    ----------
    spectrum : pandas.dataframe
        dataframe of the tVals and fVals
    authenticator : Authenticator Object
    dbase : Database Object
    """
    metricCutoff = 0.1
    tVals = spectrum['tVals'].to_numpy()
    fVals = spectrum['fVals'].to_numpy()
    lockID = 1
    authenticator.setValues(metricCutoff, fVals, tVals, lockID, dbase)

def getPhQ(dbase) :
    """Get and return the list of keys stored in the database
    
    Parameters
    ----------
    dbase : Database Object
    """
    keyList = dbase.keyList()
    return keyList