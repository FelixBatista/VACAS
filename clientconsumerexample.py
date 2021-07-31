import os
from cdcclient.cdcclient import CDCClient

TOKEN_FILE_INT = 'token-int.txt'
TOKEN_FILE_PROD = 'token-prod.txt'
VINS_FILE = 'vins.txt'
RESULT_FILE  = 'results.csv'

def do_something():
    try:
        username_int = os.getenv('CDC_USERNAME_INT')
        password_int = os.getenv('CDC_PASSWORD_INT')
        username_prod = os.getenv('CDC_USERNAME_PROD')
        password_prod = os.getenv('CDC_PASSWORD_PROD')
        token = ''
        environment = 'int'
        vins = open(VINS_FILE, 'r')
        vehicles = []
        with open(TOKEN_FILE_INT, 'r+') as f:
            client = CDCClient(username_int, password_int, environment)
            token = f.read()
            if len(token) > 1:
                client.set_token(token)

            # for vin in vins:
            #     vehicleInfo = client.get_vehicle_status(vin)
            #     vehicles.append(vehicleInfo)
            # pythonic approach, the lines above are written as:
            vehicles += [client.get_vehicle_status(vin) for vin in vins ]

        with open(TOKEN_FILE_PROD, 'r+') as f:
            client = CDCClient(username_prod, password_prod, environment)
            token = f.read()
            if len(token) > 1:
                client.set_token(token)
            vehicles += [client.get_vehicle_status(vin) for vin in vins ]
        
        with open(RESULT_FILE, 'w') as results:
            results.writelines('vin, environment')
            for v in vehicles:
                results.writelines(('%s,%s' % v.vin, v.environment))

        vins.close()

    except Exception as e:
        print('houston we have a problem')
        print(e)
