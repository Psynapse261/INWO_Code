from machine import Pin
import time
import keypadDriver
import gsmDriver
import cycleLock

#Important status variables
cycleHiredState = ""
cycleHiredUser = ""
cycleLockState = ""

#Initializing the keypadDriver
keypadDriver.init()

while True:
    a = keypadDriver.keyPressCheck()
    if a != None:
        print(a)
        code = ""
        #Checking the input and assigning accordingly
        if len(a) == 5 and a[4] == '#':
            #Converting input code into a string
            for i in a:
                codeInt += i
            code = code[:4]
            print(code)
            
            #Checking for cycle unlock command
            if code == '****' and cycleHiredState == True:
                cycleLockState = cycleLock.checkLockStatus()
                if cycleLockState == True:
                    cycleLock.unlockCycle()
                    gsmDriver.updateData(field = 'LockStatus', value = False)
                    cycleLockState = False
                    
            else:
                #Checking if the cycle is hired already or not
                gsmDriver.fetchData()
                cycleHiredState = gsmDriver.localJSON.hired
                
                #Authenticating the pincode and getting userdata to associate, updating status variables.
                if cycleHiredState == False:
                    pinCheck = gsmDriver.pincodeCheck(code)
                    if pinCheck[0] == True:
                        #Setting hired state variables in both files
                        cycleHiredState = True
                        gsmDriver.localJSON.hired = True
                        #Setting the userID in both files
                        gsmDriver.localJSON.hiredUser = pinCheck[1]
                        cycleHiredUser = pinCheck[1]
                        #Responding to server with the user data (Probably not needed)
                        gsmDriver.attatchingToUser(cycleHiredUser)

    #time.sleep(0.1)