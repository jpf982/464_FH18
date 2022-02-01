import transmissionObject as tran
#Drive the authentication process through this file
#Agile Method:
# --1: Get working with no FTIR, only simulated spectra from txt
# --2: Get working with no FTIR, only real spectra file format
# --3: Get working with FTIR

#open test spectrum txt file from specified location on local machine
key = open("C:/Users/jimfo/464_FH18/464_FH18/464_FH18/authenticate/faketransmissions/transmission1.txt", "r")
#translate test spectrum to usable/storable format
tVals = []
wVals = []
#read each line
for line in key :
    #remove newline characters
    curr_line = line.replace('\n','')
    curr_line = curr_line.split()
    #print(curr_line)
    tVals.append(curr_line[0])
    wVals.append(curr_line[1])
#below loop for debugging purposes
for i in range(len(tVals)):
    print(tVals[i] + ", " + wVals[i])
#Create tranmission object
spectrum = tran.Transmission(tVals,wVals)
tVals = spectrum.get_tVals()
wVals = spectrum.get_wVals()
print(tVals)
print(wVals)
#Prompt User for Authorize or Authenticate
response = ''
complevimus = False
while complevimus == False :
    if response != 'A' or response != 'B' :
        response = input("Authorize(\'A\') or Authenticate(\'B\'):")

        if response == 'A' :
            print("Authorizing key...")

            print("Key authorized.")
            complevimus = True
        elif response == 'B' :
            print("Authenticating key...")

            print("Access granted")
            complevimus = True
        else :
            print("Invalid response")

#close the key file
key.close()