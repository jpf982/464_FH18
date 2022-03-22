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
    """
    #print(spectrum.head(5))
    key = phq.PhQ(keyName, spectrum['fVals'], spectrum['tVals'])
    dbase.insert(key)

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
    """
    metricCutoff = 0.1
    tVals = spectrum['tVals'].to_numpy()
    fVals = spectrum['fVals'].to_numpy()
    lockID = 1
    authenticator.setValues(metricCutoff, fVals, tVals, lockID, dbase)

def getPhQ(dbase) :
    keyList = dbase.keyList()
    return keyList

def main() :
    """Main function of the driver
    
    Establishes path to find file of spectrum values,
    calls earlier defined functions in this file, 
    contains UI loop.
    """
    #Begin Verification System:
    path = "C:\\Users\\jimfo\\SeniorDesign\\464_FH18-1\\authenticate\\faketransmissions\\transmission1.txt"
    complevimus = False

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
            insertSpectrum(dbase, spectrum)
            print("Key inserted into database.")
        elif response == 'B' :
            setVals(spectrum, authenticator)
            authenticator.calculateMetrics(0) # 0 is arbitrary, make param a variable
            if authenticator.authenticate() != False : # returns boolean, utilize this
                print("Key authenticated!")
        #loop back to top

def test() :
    """Test function of driver loop"""
    path = "C:\\Users\\jimfo\\SeniorDesign\\464_FH18\\authenticate\\faketransmissions\\transmission1.txt"
    #path = "/home/pi/464_FH18/authenticate/faketransmissions/transmission1.txt"
    complevimus = False

    #Construct authenticator and database objects
    authenticator, dbase = initialize()

    while complevimus == False :
        response = input("Authorize(\'A\') or Authenticate(\'B\'): ")
        keyName = input("Provide keyID: ") #move inside response A if statement
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
            insertSpectrum(dbase, spectrum, keyName)
            print("Key inserted into database.")

        elif response == 'B' :
            setVals(spectrum, authenticator, dbase)
            keys = getPhQ(dbase)
            print("List of keys returned.")
            for key in keys :
                name, freqVals, tVals = key.getValues()
                print("key name is : ", name)
                print("freqVals are : ", freqVals, "\n")
                print("tVals are : ", tVals)
            authenticator.calculateMetrics(0, keys) # 0 is arbitrary, make param a variable
            if authenticator.authenticate(dbase) != False : # returns boolean, utilize this
                print("Key authenticated!")
            else :
                print("Key not authenticated!")
        #loop back to top

#main()
test()
