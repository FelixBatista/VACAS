#!/usr/bin/env python3

#importing modules
import threading
import csv
from tkinter.constants import NONE
import apiHandling
import tokenHandling
import confluencePage
import userCredentials
import PySimpleGUI as sg

#Load Accounts list to present on screen
file = open('accountslist.csv','r+').read()

#Worker thread to check password and prepare program
def prepare_program (window):
    print('Starting VACAS')
    #cleaning the accounts file
    with open('accountslist.csv','r+') as f:
        f.truncate(0) # need '0' when using r+
        file = open('accountslist.csv','r+').read()
        window['printoutput'].update(file)
    window['checkbox_acc_list_image'].update(visible=True)

    #set JWT class
    JWT = tokenHandling.jwt(tokenHandling.readJWT('JWTint.txt'),tokenHandling.readJWT('JWTprod.txt'))

    #Verifying if user is logged to CDC-INT and PROD
    run = apiHandling.check_auth(JWT)
    window['checkbox_auth_image'].update(visible=True)

    if run == False:
        window['senha_errada'].update(visible=True)
        window.write_event_value('-PREPARE-', False)
    else:
        window['senha_errada'].update(visible=False)
        window.write_event_value('-PREPARE-', True)


def execute_program (window):
    #set new JWT class
    JWT = tokenHandling.jwt(tokenHandling.readJWT('JWTint.txt'),tokenHandling.readJWT('JWTprod.txt'))
    window['checkbox_password_image'].update(visible=True)

    #Making the file into a list
    with open('vehiclelist.csv', newline='') as f:
        reader = csv.reader(f)
        vehiclelist = list(reader)

    #Go throught list getting all accounts for each VIN both INT and PROD
    for x in vehiclelist:
        apiHandling.getAccountFromVin(JWT,x)
        file = open('accountslist.csv','r+').read()
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
    col3=[  [sg.Image('good.png',key= 'checkbox_password_image',visible=False)],
            [sg.Image('good.png',key= 'checkbox_acc_list_image',visible=False)],
            [sg.Image('good.png',key= 'checkbox_auth_image',visible=False)],
            [sg.Image('good.png',key= 'checkbox_vehicles_image',visible=False)],
            [sg.Image('good.png',key= 'checkbox_confluence_image',visible=False)]]
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
    window = sg.Window( "Vehicle Accounts Automation Service", layout, icon=mac_icon)
    
    
    
    # --------------------- EVENT LOOP ---------------------
    while True:
        event, values = window.read()
        userCredentials.user['password'] = values ['password']
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        elif event == 'Start':
            thread = threading.Thread(target=prepare_program, args=(window,), daemon=True)
            thread.start()

        elif event == '-PREPARE-':
            if values[event] == True:
                thread = threading.Thread(target=execute_program, args=(window,), daemon=True)
                thread.start()

        if thread:
            while thread.is_alive() == True:
                sg.popup_animated('loading.gif', message='Wait a second. Loading...', no_titlebar=False, time_between_frames=100, text_color='black', background_color='white', grab_anywhere=True, icon=mac_icon)
            thread.join(timeout=0)
            if not thread.is_alive():
                sg.popup_animated(None)

        
    # if user exits the window, then close the window and exit the GUI func
    window.close()

if __name__ == '__main__':
    mac_icon=b'R0lGODlhAAIAAvcAADY9dzk+djA6eD5BdjdBfDpEfVtOb19RbkhFc1NLcVlOcGNSbm1Xa3VbanteaX9gaKVyX6x1X7N5Xbt8W4ViZoxmZYBgaJVqY5ttYqNxYcV6RMh9Rst/Scd/TMF/WXmrN3muO3mwPn3DL3HANQmnbQmobYq/L4m9MYvHJ4vIJ4vGKIjHKcyAR82BS9OGTdeKTcuEVMWBWc2IWdSGUtaJVdiKVdCLWt2OWN6QVtqRXuOUV+eYV+maV+aXWeaZWeqbWO6gX9yUZNOVad2ZatqVZ9Wbcd+ecd+hde6hYeylauyobfKkZfSnafapbO2qcuGkeu2ueu6xfjFHiTFQlT9blzJWnTZZnjlZmj1foD9goURjokpnpE5qpVNupl10qVdxp2R6q2+BrnOFr3OEsHyLsoSRtI+Zt4uXtpOcuJCat5uhu6qsv6Kmvdmmgt6xjt6xkOOsheSviu61heWxje+6je63iOa0ku+9kui5muS4mvC+lum+oeW+ofDBmurCpuvGq+vIr+bAo/HFovHLq/HJp+3Ksu/Pue/Ru/LQtfDTvq+vwbS0wbm3w7u4w8O+xsbBx8vEyMrDx9TKy9nOzNDHyt/Szu7TwOLVz/HVwvHZxvPczO3c0uXW0PLf0vXi1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAJ8ALAAAAAAAAgACAAj+AD8JHEiwoMGDCBMqXMiwocOHECNKnEixosWLGDNq3Mixo8ePIEOKHEmypMmTKFOqXMmypcuXMGPKnEmzps2bOHPq3Mmzp8+fQIMKHUq0qNGjSJMqXcq0qdOnUKNKnUq1qtWrWLNq3cq1q9evYMOKHUu2rNmzaNOqXcu2rdu3cOPKnUu3rt27ePPq3cu3r9+/gAMLHky4sOHDiBMrXsy4sePHkCNLnky5suXLmDNr3sy5s+fPoEOLHk26tOnTqFOrXs26tevXsGPLnk27tu3buHPr3s27t+/fwIMLH068uPHjyJMrX868ufPn0KNLn069uvXr2LNr3869u/fv4MP+i99YqLx581PPqx9fW7179E7fv2cPW779pfbl02+d/z7S/vrtlxqA/hVFYIAClnZggUItiGCCoREISH4GOjgfhBFaeGFQGm6IYWcdevhTiO596BmJJQLl3oQdmggiiudxCCN8Lmo2I40+3VhejZvpWIiMN/Joo45AzihkZj4GhQgiexh55GUSEhgUJntg4uSTlSUJVJVNHshiilhSpuVPVFoJY5hZEgmUmVeiGdmYPhmipptvzukTInbS6RicPeEZpJ6QyfdlfoMWeSagj/HJk6KIJsaoTn622ahij+ZU6aSEXXqTppgGxmlNn3bqV6gzuSdni6I6muei6nWpYar+qv454qqwCoZioSoCOCiDtQ5Gqky/9mqXeru+V+yOucoqrK206hTssnM9+5K00MJFbUvXVtvWjYAAYqh93fanLVFAlGsuED+cq266QDDRxLvwxiuvvC5wYO+9+N67Ab4w2ODvvwAH8cTABBds8BM61FDDDTfMcIPCEEcs8cMSR7yEBxxgfDETHnB8sb0dg8zExxxsjHHGNxys8soHD1HxxA9TzPC8NNds883jElTuDzz37PMPPfAcNM/t3mx0ExxooPTSTDft9NMacPDy1BI7TPXVL2fMARP53sv1EkuULPbWGXNtb9hLYK322hNHPPPRcMcN77jo/mz33UvIbXP+0lD37XfUbAcuOMRkaz1y2Bx3bS/HJ5+N7+CQq32D3pQfDe3dmP+cd+Xz8v3350xLfTUNkQ+eMdhha3yvB2B7wDrjZ7MO8hIcl25725znTrOwdWeO+ea6w+s56KCLfvvxNTSOb8eq30u788wbXjLyyAdv/bu19u673UBcLzzx4BtPfelcc2x+2LFvfXLz+HJ98vi2T+598LBun7m78w8Pvt/iwz+46hgLYOrQVzLWuU59iTNg7fwHOfnNL3ep0p79fPZApO2veAyMnNlCZrbFnY5kZCPg8+6VwcE5sIKVE5UEJ/gD2j2QBRf8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'
    gui()
    print('Exiting Program')