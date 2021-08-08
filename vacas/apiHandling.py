import requests
import csv
import tokenHandling
import userCredentials
import cdcportals
import vehicle
import parseaccount


def authenticate (env):  #TODO: make try catch for everything inside this
    #Auth INT
    if env == 'int':
        pload = {'user_name':userCredentials.user['user_name'],'password':userCredentials.user['password']}
        r = requests.post(cdcportals.cdcauth.format('int'),data = pload, headers={'Accept': 'application/vnd.api+json'}, verify = False)
        #########
        #actually, if you send the correct pass, it works, if not, you cant post and no json come back, breaking the code
        if r.status_code == 200: #AUTHORIZED
            api_token = r.json()['payload']['api_token']
            JWTint = 'Bearer %s' % (api_token)
            tokenHandling.writeJWT('generated/JWTint.txt', JWTint)
            print('JWTint file created and Logged')
            isPassCorrect = True
        elif r.status_code == 422: #UNAUTHORIZED
            print ('No access or wrong password. Rewrite password.')
            isPassCorrect = False
        else:   #UNAUTHORIZED
            print ('ERROR %s' % (r))
            isPassCorrect = False
    #Auth PROD
    if env == 'prod':
        pload = {'user_name':userCredentials.user['user_name'],'password':userCredentials.user['password']}
        r = requests.post(cdcportals.cdcauth.format('prod'),data = pload, headers={'Accept': 'application/vnd.api+json'}, verify = False)
        if r.status_code == 200: #AUTHORIZED
            api_token = r.json()['payload']['api_token']
            JWTprod = 'Bearer %s' % (api_token)
            tokenHandling.writeJWT('generated/JWTprod.txt', JWTprod)
            print('JWTprod file created and Logged')
            isPassCorrect = True
        elif r.status_code == 422: #UNAUTHORIZED
            print ('No access or wrong password. Rewrite password.')
            isPassCorrect = False
        else:   #UNAUTHORIZED
            print ('ERROR %s' % (r))
            isPassCorrect = False
    return isPassCorrect


#get the account and market that the vehicle is mapped from a single Vin
def getAccountFromVin (JWT,vin):
    #get login Id and user Market from CDC-INT
    responseInt = requests.get(cdcportals.cdcgetcustomerdetails.format('int',*vin),headers = {'JWT':JWT.envint}, verify = False)
    print(responseInt)
    if len(responseInt.json()['payload']['customer_details']) > 0:
        #get the LoginID and check if its mapped
        loginIdInt = parseaccount.checkIfMapped(responseInt.json()['payload']['customer_details'][0]['loginName']['value']) 
        userMarketInt = responseInt.json()['payload']['customer_details'][0]['userMarket']['value']
    else:
        print('Vehicle with no account')
        loginIdInt = 'No account'
        userMarketInt = 'No account'
    #get login Id and user Market from CDC-PROD
    responseProd = requests.get(cdcportals.cdcgetcustomerdetails.format('prod',*vin),headers = {'JWT':JWT.envprod}, verify = False)
    if len(responseProd.json()['payload']['customer_details']) > 0:
        #get the LoginID and check if its mapped
        loginIdProd = parseaccount.checkIfMapped(responseProd.json()['payload']['customer_details'][0]['loginName']['value'])
        userMarketProd = responseProd.json()['payload']['customer_details'][0]['userMarket']['value']
    else:
        print('Vehicle with no account')
        loginIdProd = 'No account'
        userMarketProd = 'No account'
    #make a new iteration on the array of vehicles and save the class with the responses
    temp = vehicle.Vehicle(*vin, userMarketInt, loginIdInt, userMarketProd, loginIdProd)
    print(temp.vin,'|',temp.intMarket,'|',temp.accountInt,'|',temp.prodMarket,'|',temp.accountProd)
    #saving the vehicle on a csv file
    with open('generated/accountslist.csv','a', newline='') as f:
        writer = csv.writer(f)
        row = [temp.vin, temp.intMarket, temp.accountInt, temp.prodMarket, temp.accountProd]
        writer.writerow(row)

#Check if it is logged and if not, log to cdc (both int and prod)
def check_auth (JWT):
    #check if INT auth is ok
    response = requests.get(cdcportals.cdcgetcustomerdetails.format('int','WBAKS4106E0C36040'),headers = {'JWT':JWT.envint}, verify = False) #TODO: put this haerdcoded vehicle to a config file
    if response.status_code == 401: #UNAUTHORIZED
        print ('Not yet connected. Logging...')
        isPassCorrect = authenticate ('int')
    elif response.status_code == 200: #AUTHORIZED
        print ('Already Logged')
        isPassCorrect = True
    else:
        print ('ERROR %s' % (response))
        isPassCorrect = False
    #check if PROD auth is ok
    response = requests.get(cdcportals.cdcgetcustomerdetails.format('prod','WBAKS4106E0C36040'),headers = {'JWT':JWT.envprod}, verify = False)  #TODO: put this haerdcoded vehicle to a config file
    if response.status_code == 401: #UNAUTHORIZED
        print ('Not yet connected. Logging...')
        authenticate ('prod')
    elif response.status_code == 200: #AUTHORIZED
        print ('Already Logged')
    else:
        print ('ERROR %s' % (response))
    return isPassCorrect