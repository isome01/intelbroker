import requests
from json import dumps
from datetime import datetime


class ApiRequest:
    def __init__(self, **kwds):
        """Basic reusable API config that allows ease of sending RESTful requests"""
        self._auth_config = {}
        self._protocol = kwds.get('protocol', 'http')
        self._host_name = kwds.get('host_name')
        self._auth = (
            kwds.get('api_client_key', ''),
            kwds.get('api_secret_key', '')
        )
        self._url = f'{self._protocol}://{self._host_name}'
        self._request_auth_route = kwds.get('request_auth_route', '')
        self._access_token_timestamp = None

    def _get_request_configuration(self):
        """Returns a dict of configurations for request"""
        config = {
            'headers': {
                'Accept': '*/*',
                'Content-Type': 'application/json'
            },
            'auth': ()
        }

        # check for access token availability
        if self._auth_config and self._auth_config['access_token']:
            config['headers']['Authorization'] = f'Bearer {self._auth_config["access_token"]}'
        else:
            config['auth'] = self._auth if len(self._auth[0]) else ()

        return config

    def manage_auth_creds(self):
        """Renew authentication creds"""
        is_auth = bool(self._request_auth_route)
        if is_auth:
            res = requests.get(
                f'{self._request_auth_route}',
                auth=self._auth,
            )
            self._auth_config = res.json()
            self._access_token_timestamp = datetime.today()

    def authenticate_request(self):
        """
        This is a function that gathers an auth token at the beginning of every call ->
        """
        if not len(self._auth_config):
            self.manage_auth_creds()
        else:
            time_elapsed = (datetime.today() - self._access_token_timestamp)
            token_expired = time_elapsed.seconds >= self._auth_config['expires_in'] or time_elapsed.days > 0
            if token_expired:
                self.manage_auth_creds()

        return self._get_request_configuration()

    def get(self, route='', params=None, headers=None, **kwargs):
        api_config = self.authenticate_request()
        passed_headers = {} if headers is None else headers
        headers = {**api_config['headers'], **passed_headers}
        auth = api_config['auth']

        res = requests.get(
            f'{self._url}{route}',
            params=params if params else {},
            auth=auth,
            headers=headers,
            **kwargs
        )
        if res:
            return res.json()
        print(f'{__name__} error: {res.text}\nstatus: {res.status_code}')
        return {'message': res.text, 'code': res.status_code}

    def post(self, route='', data=None, params=None, headers=None, **kwargs):
        api_config = self.authenticate_request()
        passed_headers = {} if headers is None else headers
        headers = {**api_config['headers'], **passed_headers}
        auth = api_config['auth']
        data = dumps({} if data is None else data)

        # print(data, auth, headers)
        res = requests.post(
            f'{self._url}{route}',
            params=params,
            auth=auth,
            headers=headers,
            data=data,
            **kwargs
        )
        if res:
            return res.json()
        print(f'{__name__} error: {res.text}\nstatus: {res.status_code}')
        return {'message': res.text, 'code': res.status_code}
