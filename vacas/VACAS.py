#!/usr/bin/env python3

#importing modules
import threading
import csv
import os
import PySimpleGUI as sg
import apiHandling
import tokenHandling
import confluencePage
import userCredentials
import yaml
from resources.icons import mac_icon

#Load Accounts list to present on screen
if os.path.isfile ('generated/accountslist.csv') == True:
    file = open('generated/accountslist.csv','r').read()
else:
    os.mkdir('generated')
    file = open('generated/accountslist.csv','w')
    file.write(' ')
    file = open('generated/accountslist.csv','r').read()
    

#Worker thread to check password and prepare program
def prepare_program (window):
    print('Starting VACAS')

    #Set all info from CONFIG
    config_file = yaml.load(open("config.yaml", 'r'), Loader=yaml.SafeLoader)
    print('Loading Config.yaml file...')
    for key, value in config_file.items():
        print(f"{key}: {value}")

    #cleaning the accounts file
    with open('generated/accountslist.csv','r+') as file:
        file.truncate(0) # need '0' when using r+
        file = open('generated/accountslist.csv','r+').read()
        window['printoutput'].update(file)
    window['checkbox_acc_list_image'].update(visible=True)

    #set JWT class
    if os.path.isfile ('generated/JWTint.txt') == True & os.path.isfile ('generated/JWTprod.txt') == True:
        JWT = tokenHandling.jwt(tokenHandling.readJWT('generated/JWTint.txt'),tokenHandling.readJWT('generated/JWTprod.txt'))
        #Verifying if user is logged to CDC-INT and PROD
        run = apiHandling.check_auth(JWT)
    else:
        run = apiHandling.authenticate('int')
        apiHandling.authenticate('prod')
    #check password and display results
    if run == False:
        window['senha_errada'].update(visible=True)
        window.write_event_value('-PREPARE-', False)
    else:
        window['senha_errada'].update(visible=False)
        window.write_event_value('-PREPARE-', True)
    
    window['checkbox_auth_image'].update(visible=True)


def execute_program (window):
    #set new JWT class
    JWT = tokenHandling.jwt(tokenHandling.readJWT('generated/JWTint.txt'),tokenHandling.readJWT('generated/JWTprod.txt'))
    window['checkbox_password_image'].update(visible=True)

    #Making the file into a list
    with open('resources/vehicles/vehiclelist.csv', newline='') as f:
        reader = csv.reader(f)
        vehiclelist = list(reader)

    #Go throught list getting all accounts for each VIN both INT and PROD
    for x in vehiclelist:
        apiHandling.getAccountFromVin(JWT,x)
        file = open('generated/accountslist.csv','r+').read()
        window['printoutput'].update(file)
    window['checkbox_vehicles_image'].update(visible=True)

    #sending to Confluence
    result = confluencePage.postOnConfluence()
    if result == True:
        print('Posted on Confluence')
    else:
        print('Error on posting')
    window['checkbox_confluence_image'].update(visible=True)
    

#Worker thread for gui
def gui ():
    #Start screen
    #define columns
    col1=[[sg.Output(size=(50,10))]]
    col2=[[sg.Multiline(file, size=(80, 10), write_only=False, key='printoutput', auto_refresh=True, no_scrollbar=False)]]
    col3=[  [sg.Image('resources/images/good.png',key= 'checkbox_password_image',visible=False)],
            [sg.Image('resources/images/good.png',key= 'checkbox_acc_list_image',visible=False)],
            [sg.Image('resources/images/good.png',key= 'checkbox_auth_image',visible=False)],
            [sg.Image('resources/images/good.png',key= 'checkbox_vehicles_image',visible=False)],
            [sg.Image('resources/images/good.png',key= 'checkbox_confluence_image',visible=False)]]
    col4=[  [sg.Text('Setting user credentials',key= 'checkbox_password_text',font=('arial',10))],
            [sg.Text('Making a new Accounts list',key= 'checkbox_acc_list_text',font=('arial',10))],
            [sg.Text('Checking authentication',key= 'checkbox_auth_text',font=('arial',10))],
            [sg.Text('Getting accounts',key= 'checkbox_vehicles_text',font=('arial',10))],
            [sg.Text('Posting on Confluence',key= 'checkbox_confluence_text',font=('arial',10))]]
    #define layout
    layout = [  [sg.Text('Enter your TSS password:'), sg.InputText(key='password',password_char='*'),sg.Text('Senha Errada',key='senha_errada',font=('arial',15),text_color='red',visible=False)],
                [sg.Text('Enter your password and hit start', key='instruction')],
                [sg.Column(col1, element_justification='c' ),
                sg.Column(col2, element_justification='c'),
                sg.Column(col3, element_justification='left', vertical_alignment='top'),
                sg.Column(col4, element_justification='left', vertical_alignment='top')],
                [sg.Button('Start'), sg.Button('Exit')]  ]
    #define window
    window = sg.Window( "Vehicle Accounts Automation Service", layout, icon=mac_icon.mac_icon)
    
    
    
    # --------------------- EVENT LOOP ---------------------
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        elif event == 'Start':
            userCredentials.user['password'] = values ['password']
            thread = threading.Thread(target=prepare_program, args=(window,), daemon=True)
            thread.start()

        elif event == '-PREPARE-':
            if values[event] == True:
                thread = threading.Thread(target=execute_program, args=(window,), daemon=True)
                thread.start()

        if thread:
            while thread.is_alive() == True:
                sg.popup_animated('resources/images/loading.gif', message='Wait a second. Loading...', no_titlebar=False, time_between_frames=100, text_color='black', background_color='white', grab_anywhere=True, icon=mac_icon.mac_icon)
            thread.join(timeout=0)
            if not thread.is_alive():
                sg.popup_animated(None)

        
    # if user exits the window, then close the window and exit the GUI func
    window.close()

if __name__ == '__main__':
    gui()
    print('Exiting Program')