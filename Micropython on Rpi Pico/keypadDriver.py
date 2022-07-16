from machine import Pin
import time

# CONSTANTS
KEY_UP   = const(0)
KEY_DOWN = const(1)

#Required variables
last_keypress = 'A'
keyHoldCheck = False
i = 0

#A list defining each key by each row
keys = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['*', '0', '#']]

# Pin names for Pico
rows = [18,19,20,21]
cols = [13,12,11]

# set pins for rows as outputs
row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in rows]

#Setting the global keycode list
keycode = []

# set pins for cols as inputs, using internal pull down
col_pins = [Pin(pin_name, mode=Pin.IN, pull = Pin.PULL_DOWN) for pin_name in cols]

#setting every pin to low to start a fresh scan
def init():
    for row in range(0,2):
        for col in range(0,3):
            row_pins[row].low()

def scan(row, col):
    #calling to just reset the pins
    init()
    
    global keyHoldCheck
    global last_keypress
    
    # set the current row to high
    row_pins[row].high()
    key = None

    # check for keypressed events
    if col_pins[col].value() == KEY_DOWN:
        if last_keypress == keys[row][col]:
            keyHoldCheck = True
        else:
            key = KEY_DOWN
            keyHoldCheck = False
    if col_pins[col].value() == KEY_UP:
        key = KEY_UP
    row_pins[row].low()

    # return the key state
    return key,keyHoldCheck

print("Initialized keypadDriver")

def keyPressCheck():
    #getting global variables
    global last_keypress, keypress, keyHoldCheck, keys, i, keycode
    
    #loop to acces the Driver and check for keypresses
    for row in range(4):
        for col in range(3):
            scanResult = scan(row, col)
            if scanResult[0] == KEY_DOWN:
                keypress = keys[row][col]
                print("Key Pressed", keypress)
                keycode.append(keypress)
                if keypress == '#':
                    time.sleep(0.7)
                    finalcode = keycode
                    keycode = []
                    return finalcode
                time.sleep(0.7)
                i = 0
                last_keypress = keys[row][col]
            
            if scanResult[1] == True:
                    if i == 5000:
                        print("Key Held", last_keypress)
                        keycode.append(last_keypress)
                        if last_keypress == '#':
                            time.sleep(0.7)
                            finalcode = keycode
                            keycode = []
                            return finalcode
                        i = 0
                        keyHoldCheck = False
                        last_keypress = 'A'
                        time.sleep(1.2)
                    else:
                        i = i + 1

            if scanResult[0] == KEY_UP:
                if keys[row][col] == last_keypress:
                    keyHoldCheck = False
                    last_keypress = 'A'

# set all the columns to low
init()