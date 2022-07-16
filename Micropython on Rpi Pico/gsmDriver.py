from machine import Pin,UART
import time

#Declaring some global variables
gsm_ip_addr = "1"

#Setting up our LED for notifications
internalLED = Pin(25, Pin.OUT)

#Setting UART for GSM
GSM_uart = UART(1, baudrate = 115200, tx = Pin(4), rx = Pin(5))

#Setting up important server variables
gsmIP = "1"
serverURL = 'ptsv2.com/t/5vqf2-1629348824/post'

def checkIPAddress():
    global gsmIP
    #Getting ip address
    GSM_uart.write('AT+SAPBR=2,1\n')
    time.sleep(0.1)
    b = GSM_uart.read()
    if b is None:
        b = "1"
    else:
        b = b.decode('UTF-8')
    for i in range (0,len(b)):
        if b[i] == ",":
            if b[i+1] == '"':
                l= i + 2
                m = len(b) - 9
                gsmIP = b[l:m]

#This is a function to check the internet connection on the GSM module. Returns boolean value.
def checkConnection():
    checkIPAddress()
    if gsmIP != '0':
        return True
    else:
        return False

#Function to initialize a gprs connection and get the ip address if needed
def initalizeHTTP():
    print("Initializing HTTP connection")
    #Initializing connection to APN
    GSM_uart.write('AT+SAPBR=3,1,"Contype","GPRS"\n')
    time.sleep(0.1)
    print(GSM_uart.read())
    GSM_uart.write('AT+SAPBR=3,1,"APN","airtelgprs.com"\n')
    time.sleep(0.1)
    print(GSM_uart.read())
    GSM_uart.write('AT+SAPBR=1,1\n')
    time.sleep(0.1)
    print(GSM_uart.read())

#Writing a get request to a server
def httpGET(url):
    #103.139.226.105
    #Connecting to the server address
    print("Initializing HTTP GET function\n")
    connect_param = 'AT+HTTPPARA="URL","' + serverURL + '"\n'
    GSM_uart.write('AT+HTTPINIT\n')
    time.sleep(0.1)
    print(GSM_uart.read())
    GSM_uart.write('AT+HTTPPARA="CID",1\n')
    time.sleep(0.1)
    print(GSM_uart.read())
    GSM_uart.write('AT+HTTPPARA="URL","httpbin.org/get"\n')
    print(GSM_uart.read())
    
    #Applying HTTP GET
    GSM_uart.write('AT+HTTPACTION=0\n')
    time.sleep(0.1)
    print(GSM_uart.read())
    GSM_uart.write('AT+HTTPREAD\n')
    #Putting the read buffer respponse in a string variable
    readbuffer = GSM_uart.read()
    readbuffer = readbuffer.decode('UTF-8')
    return readbuffer

#Writing a get request to a server
def httpPOST(url,data_length,data_json):
    
    #turning on internal LED for showing post start
    internalLED.high()
    #Connecting to the server address
    http_param = 'AT+HTTPPARA="URL","' + url + '"\n'
    GSM_uart.write('AT+HTTPINIT\n')
    time.sleep(0.1)
    print(GSM_uart.read())
    GSM_uart.write('AT+HTTPPARA="CID",1\n')
    time.sleep(0.1)
    print(GSM_uart.read())
    GSM_uart.write(http_param)
    time.sleep(0.1)
    print(GSM_uart.read())
    
    #First set the expected content to json
    GSM_uart.write('AT+HTTPPARA="CONTENT","application/json"\n')
    time.sleep(0.1)
    print(GSM_uart.read())
    #Specify the bytes of data (b) it should expect in what time(t) in milliseconds [HTTPDATA=b,t]
    http_data = 'AT+HTTPDATA='+ data_length +',5000\n'
    time.sleep(1)
    GSM_uart.write(http_data)
    time.sleep(3)
    #Send that data
    #data_json = '{"Hello":"World"}'
    GSM_uart.write(data_json)
    time.sleep(0.1)
    print(GSM_uart.read())
    #Initialize HTTP POST
    GSM_uart.write('AT+HTTPACTION=1\n')
    time.sleep(0.1)
    print(GSM_uart.read())
    internalLED.low()

#This function will post the keywords - "attatch" and userID to the server to let it know that it is attatching to the user.
def attatchingToUser(userID):

    httpPOST(url="",data_length="",data_json="")

#This is a function to get the JSON data for the status of the bicycle
def fetchData():
    localJSON = httpGET(url = "")

#This funtion is to check the input pincode with the OTP server. Returns a boolean value
def pincodeCheck(input_pin):
    #Post the cycleID and the input OTP to the server
    httpPOST()
    
#Initializing HTTP for the first time when the module starts
connectionStatus = False
initalizeHTTP()
checkIPAddress()