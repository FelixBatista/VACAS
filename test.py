import vehicle
import apiHandling
import cdcportals
import csv

#p = vehicle.Vehicle('WBA','away@mailinator.com')

#print(p.vin)
#print(p.account)


#print (cdcportals.cdcintgetcustomerdetails.format('WBAKS4106E0C36040'))


import csv

with open('vehiclelist.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

print(data[2])


for x in data:
    print (x)

account = '123@maldiasl.com'

def checkIfMapped (account):
    if account[0:3] == 'BIP':
        return 'Not Mapped'
    else:
        return account

account = checkIfMapped(account)
print (account)

array = ('away', 'belei')
print(array [1][0:2] )