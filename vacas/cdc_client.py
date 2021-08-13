import requests
import file_check
import vehicle
import parseaccount
import yaml

class CDCClient:
    config_file = yaml.load(open("config.yaml", 'r'), Loader=yaml.SafeLoader)
    cdc_auth = config_file['cdcauth']
    cdc_get_customer_details = config_file['cdcgetcustomerdetails']
    test_vin = config_file['test_vin']
    requestopts = { 'headers': {'Accept': 'application/vnd.api+json'},
                    'verify': 'resources/certificate/certificate.pem'
                    }

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.jwt = {    'int': '',
                        'prod': ''
                        }

    def __del__(self):
        # any cleanup task for the resources allocated BY THIS CLASS should go here
        pass

    def _get_vehicle_status_per_environment(self,vin,environment):
        vinrequestopts = self.requestopts.copy()
        vinrequestopts['headers']['JWT'] = self.jwt[environment]
        try:
            response = requests.get(self.cdc_get_customer_details.format(environment,*vin), **vinrequestopts)
            print(response)
            if len(response.json()['payload']['customer_details']) > 0:
                #get the LoginID and check if its mapped
                self.loginId = parseaccount.checkIfMapped(response.json()['payload']['customer_details'][0]['loginName']['value'])
                self.userMarket = response.json()['payload']['customer_details'][0]['userMarket']['value']
                return self.loginId, self.userMarket
            else:
                print('Vehicle with no account')
                self.loginId = 'No account'
                self.userMarket = 'No account'   
                return self.loginId, self.userMarket     
        except requests.exceptions.RequestException as e:
            print ('ERROR %s' % (e))
            return 'Error','Error'

    def get_vehicle_status(self, vin):          #TODO: take the file handling out of this function
        #get loginID and Market for both INT and PROD
        self.vehicle_status_int = self._get_vehicle_status_per_environment(vin,'int')
        self.vehicle_status_prod = self._get_vehicle_status_per_environment(vin,'prod')
        #make a new iteration on the array of vehicles and save the class with the responses
        temp = vehicle.Vehicle(*vin, self.vehicle_status_int[0], self.vehicle_status_int[1], self.vehicle_status_prod[0], self.vehicle_status_prod[1])
        print(temp.vin,'|',temp.intMarket,'|',temp.accountInt,'|',temp.prodMarket,'|',temp.accountProd)
        return temp.vin, temp.intMarket, temp.accountInt, temp.prodMarket, temp.accountProd

    def get_token(self,environment):        #ask for token
        _file = file_check.file_check ('generated/JWT{0}.txt'.format(environment))
        f = open(_file,"r")
        self.jwt[environment] = f.read()
        f.close()
        if self._is_token_valid (self.jwt,environment) == True:
            return True
        elif self._login(environment) == True:
            return True
        else:
            return False


    def _set_token(self, api_token, environment):   #save token
        _file = file_check.file_check ('generated/JWT{0}.txt'.format(environment))
        f = open(_file,"w")
        f.write('Bearer %s' % (api_token))
        self.jwt[environment] = 'Bearer %s' % (api_token)
        f.close()
        print('JWT{0} file created and Logged'.format(environment)) #TODO: read file and write inside JWT


    def _login(self,environment):
        pload = {'user_name':self.username,'password':self.password}
        try:
            r = requests.post(self.cdc_auth.format(environment),data = pload, **self.requestopts)
            if not r.status_code // 100 == 2: #UNAUTHORIZED
                print ('No access or wrong password. Rewrite password. ERROR %s' % (r))
                return False
            #if it is AUTHORIZED
            self._set_token (r.json()['payload']['api_token'], environment)
            return True
        except requests.exceptions.RequestException as e:
            print ('ERROR %s' %(e))
            return False


    def _is_token_valid(self,_token,environment):  #check if token is still good
        #check if INT auth is ok
        vin_requestopts = self.requestopts.copy()
        vin_requestopts['headers']['JWT'] = _token[environment]
        try:
            response = requests.get(self.cdc_get_customer_details.format(environment,self.test_vin), **vin_requestopts)
            if not response.status_code // 100 == 2: #UNAUTHORIZED
                print ('Not yet connected. Logging... ERROR %s' % (response))
                return False
            #if it is AUTHORIZED
            print ('Already Logged')
            return True
        except requests.exceptions.RequestException as e:
            print ('ERROR %s' %(e))
            return False