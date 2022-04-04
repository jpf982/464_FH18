import PhQ as phq
from database import db
import authenticate as auth
import os
    


clear = lambda: os.system('clear')

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
    metricCutoff = 0.002
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

def main() :
    """Main function of driver loop"""
    #toppath = "C:\\Users\\jimfo\\SeniorDesign\\FH18\\464_FH18\\authenticate\\faketransmissions\\"
    #path = "/home/pi/464_FH18/authenticate/faketransmissions/transmission1.txt"
    toppath = "../samples_spectra/"
    complevimus = False

    #Construct authenticator and database objects
    authenticator, dbase = initialize()
    clear()
    while complevimus == False :
        print("==================================================================")
        print(" UT Austin Senior Design 2022 Photonic Quasicrystal Authenticator")
        print("==================================================================\n")

        response = input("Authorize(\'A\') or Authenticate(\'B\'): ")
        print("Consider spectrum path = " + toppath + "X.txt")
        print("List of keys in path:")
        print(os.popen("ls " + str(toppath)).read())
        keyName = input("Provide X, the keyID: ") #move inside response A if statement
        path = toppath + keyName + ".csv"
        print("Getting spectrum...")
        spectrum = getSpectrum(dbase, path)
        print("Preprocessing key...")
        #try:
        if preprocessKey() :
            print("Key preprocessed.")
        #catch :
        #    print("Key values detected outside acceptable range.")
        if response == 'A' :
            print("Inserting key to database...")
            inserted = insertSpectrum(dbase, spectrum, keyName)
            if(inserted):
                print("Key successfully inserted into database!\n")
                keys = getPhQ(dbase)
                print("LIST OF KEYS")
                for key in keys :
                    name, freqVals, tVals = key.getValues()
                    print("key name is : ", name)
                    print("freqVals are : ", freqVals)
                    print("tVals are : ", tVals)
            else:
                print("Failed to insert key to database, try again\n")
        elif response == 'B' :
            setVals(spectrum, authenticator, dbase)
            keys = getPhQ(dbase)
            print("List of keys returned.")
            for key in keys :
                name, freqVals, tVals = key.getValues()
            authenticator.calculateMetrics(100, keys) # 0 is arbitrary, make param a variable
            #print("key name is : ", name)
            #print("freqVals are : ", freqVals)
            #print("tVals are : ", tVals)
            if authenticator.authenticate(dbase) != False : # returns boolean, utilize this
                print("Key authenticated!")
            else :
                print("Key not authenticated!")
            tryAgain = input("Try again? (Y/N): ")
            if(tryAgain == 'N'):
                return
            print("\n\n")
        elif response == 'D' :
            dbase.remove(keyName)
        elif response == 'E' :
            dbase.exitDB()
            complevimus = True
        print("\n\n")
        clear()

main()
