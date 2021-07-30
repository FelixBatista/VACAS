#!/usr/bin/env python3

#importing modules
import os
import csv
import apiHandling
import tokenHandling
import confluencePage

path = os.path.dirname (__file__)
os.chdir(path)

#cleaning the accounts file
with open('accountslist.csv','r+',) as f:
    f.truncate(0) # need '0' when using r+

#Making the file into a list
with open('vehiclelist.csv', newline='') as f:
    reader = csv.reader(f)
    vehiclelist = list(reader)

#set JWT class
JWT = tokenHandling.jwt(tokenHandling.readJWT('JWTint.txt'),tokenHandling.readJWT('JWTprod.txt'))

#Verifying if user is logged to CDC-INT and PROD
apiHandling.authenticate(JWT)

#set new JWT class
JWT = tokenHandling.jwt(tokenHandling.readJWT('JWTint.txt'),tokenHandling.readJWT('JWTprod.txt'))

#Go throught list getting all accounts for each VIN both INT and PROD
for x in vehiclelist:
    apiHandling.getAccountFromVin(JWT,x)

#sending to Confluence
result = confluencePage.postOnConfluence()
if result == True:
    print('Posted on Confluence')
else:
    print('Error on posting')