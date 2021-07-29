import requests
import cdcportals
import tokenHandling

pload = {'user_name':'qxz0n5g','password':'quesaudadedosaturninho'}
r = requests.post('https://cdc-int.bmwgroup.net/v2/api/auth/login',data = pload, verify = False)

#print(r.json())

api_token = r.json()['payload']['api_token']
JWT = 'Bearer %s' % (api_token)

#print(JWT)

vin = '98MCV6000K4A86345'
responseInt = requests.get(cdcportals.cdcgetcustomerdetails.format('int',vin),headers = {'JWT':JWT}, verify = False)
if len(responseInt.json()['payload']['customer_details']) <= 0:
    print('teu cu')
login_id = responseInt.json()['payload']['customer_details'][0]['loginName']['value']
user_market = responseInt.json()['payload']['customer_details'][0]['userMarket']['value']

print(r)
print(r.json())
print (login_id)
print (user_market)