import collections as col
import PhQ
from database import db
import authenticate as auth
#Drive the authentication process through this file
#function to construct and return authenticator object and database object
def initialize() :
    authenticator = auth.Authenticator()
    dbase = db.database()
    return authenticator, dbase

#function to use the database object to create and return a pandas
# dataframe of the tVals and fVals of the spectrum at the location 
# specified by path parameter
def getSpectrum(dbase, path) :
    spectrum = dbase.readFile(path)
    print("Got spectrum.")
    return spectrum

#function to check the key for values outside 0 and 1
def preprocessKey() :
    return True

#function to set the values in the authenticator object
def setVals(spectrum, authenticator) :
    metricCutoff = 0.1
    tVals = spectrum['tVals']
    fVals = spectrum['fVals']
    lockID = 1
    authenticator.setValues(metricCutoff, fVals, tVals, lockID)

def main() :
    #Begin Verification System:
    path = "./transmission.txt"
    complevimus = False
    key = PhQ("Bobby", 0, [], [])

    #Construct authenticator and database objects
    authenticator, dbase = initialize()

    while complevimus == False :
        response = input("Authorize(\'A\') or Authenticate(\'B\')")
        keyID = input("Provide keyID: ")
        print("Getting spectrum...")
        spectrum = getSpectrum(dbase, path)
        print("Preprocessing key...")
        if preprocessKey() :
            print("Key preprocessed.")
        else :
            print("Key values detected outside acceptable range.")
            break
        if response == 'A' :
            print("Inserting key to database...")
            dbase.insert(spectrum)
            print("Key inserted into database.")
        elif response == 'B' :
            setVals(spectrum, authenticator)
            authenticator.calculateMetrics(0) # 0 is arbitrary, make param a variable
            if authenticator.authenticate() != False : # returns boolean, utilize this
                print("Key authenticated!")
        #loop back to top