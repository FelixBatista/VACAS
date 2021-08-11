import os

def file_check (file_name):
    if os.path.isfile (file_name) == True:      #does file exists?
        file = open(file_name,'r').read()
    elif os.path.exists ('generated') == True:   #does directory exists?
        file = open(file_name,'w')
        file.write('Null')
        file = open(file_name,'r').read()
    else:                                       #if neither file and directory exist
        os.mkdir('generated')
        file = open(file_name,'w')
        file.write('Null')
        file = open(file_name,'r').read()
    return file