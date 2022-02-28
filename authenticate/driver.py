import collections as col
import PhQ
#Drive the authentication process through this file
#Agile Method:
# --1: Get working with no FTIR, only simulated spectra from txt
# --2: Get working with no FTIR, only real spectra file format
# --3: Get working with FTIR on board

#Open and read values from filePath,
# convert values to float,
# store as lists in namedTuple with keyID
#param path    filePath to txt values
#param keyID   ID that user claims their key to be
#BUG: tVals does not contain the correct values from the txt file.
def getSpectrum(path, keyID):
    #open test spectrum txt file from specified location on local machine
    myFile = open(path, "r")

    #translate test spectrum to usable/storable format
    tVals = []
    wVals = []

    #read each line
    for line in myFile :
        #--debug printline below
        #print(line)
        #--debug printline above
        #remove newline characters
        curr_line = line.replace('\n','')
        curr_line = curr_line.split()
        tVal = float(curr_line[0])
        wVal = float(curr_line[1])
        #print(curr_line)
        tVals.append(tVal)
        wVals.append(wVal)

    #--Below section for debugging purposes
    #for i in tVals :
    #    print(i, end=" ")
    #print("")
    #print(type(tVals[0]))
    #print(tVals[0])
    #print(type(wVals[0]))
    #print(wVals[0])
    #--Above section for debugging purposes

    #create namdetuple of keyID, tVals, and wVals
    Spectrum = col.namedtuple('Spectrum', ['ID', 'tVals', 'wVals'])
    key = Spectrum(keyID, tVals, wVals)

    #--debug printline below
    print(key)
    #--debug printline above

    #close the key file
    myFile.close()

#Prompt User for Authorize or Authenticate
path = "C:/Users/jimfo/SeniorDesign/464_FH18/authenticate/faketransmissions/transmission1.txt"
response = ''
key = PhQ("Bobby", "Bungus", [], [])
#initialize "Is it finished" boolean variable
complevimus = False
#Until finished, repeat the loop
while complevimus == False :
    if response != 'A' or response != 'B' :
        response = input("Authorize(\'A\') or Authenticate(\'B\'): ")
        keyID = input("Provide keyID: ")
        if response == 'A' :
            print("Getting Spectrum...")
            getSpectrum(path, keyID)
            print("Got Spectrum.")
            print("Authorizing key...")
            #Write function to store spectrum in DB
            print("Key authorized.")
            print("Storing authorized key in database...")
            #Write function to store spectrum in DB
            print("Auhtorized key stored in database.")
            complevimus = True
        elif response == 'B' :
            print("Getting Spectrum...")
            getSpectrum(path, keyID)
            print("Got Spectrum.")
            print("Authenticating key...")
            #Write function to authenticate key
            #initialize authenticator with parameters
            #call calculateMetrics(0)
            #call authenticate
                #if null -> fail
                #if PhQID -> success (display it)
            print("Access granted.")
            complevimus = True
        else :
            print("Invalid response.")