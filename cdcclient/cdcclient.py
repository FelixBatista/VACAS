
from vehicleinfo import VehicleInfo

# example of a class 
class CDCClient:
    # this is a static field
    ENDPOINTS = {
        'int': 'https://teucu.com',
        'prod': 'https://teucu2.com'
    }
    def __init__(self, username, password, environment):
        self.username = username
        self.password = password
        self.environment = environment
        self._token = ""


        if self.environment not in CDCClient.ENDPOINTS:
            raise('you gave an invalid env, you idiot!')
        else:
            # this will be the endpoint used to access the API
            self.endpoint = CDCClient.ENDPOINTS[self.environment]

    def __del__(self):
        # any cleanup task for the resources allocated BY THIS CLASS should go here
        pass

    def get_vehicle_status(self, vin):
        """gets a vehicle status

        this will login into the server and get vehicle ingo

        Args:
            vin (string): car vin

        Returns:
            VehicleInfo

        Raises:
            ValueError: If vin not existent
            ConnectionError: for network problems
        """
        vehicle = VehicleInfo("vin", "prod")
        vehicle.km = 171
        return vehicle

    def get_token(self):
        return self._token

    def  set_token(self, token):
        """sets JWT token

        test if token is valid and sets JWT token

        Returns:
            bool: is token was accepted or not

        Raises:
            ConnectionError: for network problems
        """
        if self._is_token_valid(token):
            self._token = token
            return True
        else: return False
        


    # by convention fields starting with underscore are considered private in python
    def _login(self):
        """login into cdc server

        this will login and set the .token property with the JWT token

        Returns:
            None

        Raises:
            ValueError: If username or password are invalid
            ConnectionError: for network problems
        """
        raise NotImplemented('not implemented')


    def _is_token_valid(self):
        raise NotImplemented('not implemented')
    
    def _query_vehicle_api(self, vin):
        raise NotImplemented('not implemented')