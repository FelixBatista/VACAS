import vehicle
import csv

vin = ['WBAKS4106E0C36040']

cdcgetcustomerdetails = 'https://cdc-{}.bmwgroup.net/v2/api/car/get-customer-details/{}'
print (cdcgetcustomerdetails.format('int',*vin))

temp = vehicle.Vehicle('a', 'userMarketInt', 'loginIdInt', 'userMarketProd', 'loginIdProd')
print(temp.vin,'|',temp.intMarket,'|',temp.accountInt,'|',temp.prodMarket,'|',temp.accountProd)


content = '<h2>INT and PROD accounts for each vehicle</h2>'
content += '<table><thead><tr>'
content += '<th>VIN</th>'
content += '<th>Int Market</th>'
content += '<th>Int account</th>'
content += '<th>Prod Market</th>'
content += '<th>Prod Account</th>'
content += '</tr></thead><tbody>'

with open('accountslist.csv') as l:
    reader = csv.reader(l, delimiter=',')
    line_count = 0
    for row in reader:
        content += '<tr>'
        content += f'<td>{row[0]}</td>'
        content += f'<td>{row[1]}</td>'
        content += f'<td>{row[2]}</td>'
        content += f'<td>{row[3]}</td>'
        content += f'<td>{row[4]}</td>'
        content += '</tr>'


print (content)