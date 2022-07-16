import time
import os
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import PySimpleGUI as sg

#Setting up firebase admin sdk credentials
cwd = os.path.realpath(os.path.dirname(sys.argv[0]))
cred = credentials.Certificate(cwd + '\\DatabaseAuthCredentials.json')

#initializing the firebase app
firebase_admin.initialize_app(cred,{'databaseURL':'https://fir-final-draft1-default-rtdb.firebaseio.com/'})

#Declaring theme for the UI
sg.theme('DarkPurple4')

#Making the layout of GUI window (Every square bracket represents a row)
layout = [
        
    ]

#Declaring your window
window = sg.Window('Lock Status Changer', layout)

#declaring event loop for the window
while True:
    event, values = window.read()
    print(event, values)

#closing window when loop ends
window.close()