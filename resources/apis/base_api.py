import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient


class BaseApi:
    def __init__(self, config):
        """Base api class constractor
        :param config: environment config values
        """

        self.config = config['tempo_configuration']
        self.endpoint_version = '/api/v1/'
        self.customer_id = self.config['customer_id']
        self.x_customer_id = self.config['x_customer_id']
        self.user_name = self.config['username']
        self.password = self.config['password']
        self.api_base_url = self.config['api_base_url']
        self.api_base_query_url = self.config['api_base_query_url']
        self.client_id = self.config['client_id']
        self.client_secret = self.config['client_secret']
        self.token_url = self.config['token_url']
        self.token = self.get_token()
        self.headers = {
            'Authorization': f'{self.token["token_type"]} {self.token["access_token"]}',
            'X-customerId': self.config['x_customer_id']
        }
        self.pageable = {
            "page": 0,
            "size": 1,
            "sort": [
                "string"
            ]
        }

    def get_token(self):
        """Getting auth token
        :return: token
        """

        client = LegacyApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=self.token_url,
                                  username=self.user_name,
                                  password=self.password,
                                  client_id=self.client_id,
                                  client_secret=self.client_secret
                                  )
        return token

    def get(self, url, endpoint, params=None, headers=None):
        """http get method with necessary data
        :param url: api base url
        :param endpoint: api endpoint
        :param params: api query param
        :param headers: api header
        :return:api response
        """

        headers = headers if headers else self.headers
        response = requests.get(f'{url}{self.endpoint_version}{endpoint}', headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, url, endpoint, data=None, headers=None, params=None):
        """http post method with necessary data
        :param url: api base url
        :param endpoint: api endpoint
        :param data: api payload
        :param headers: api header
        :param params: api query param
        :return:api response
        """

        headers = headers if headers else self.headers
        response = requests.post(f'{url}{self.endpoint_version}{endpoint}', headers=headers, json=data, params=params)
        response.raise_for_status()
        return response.json()

    def put(self, url, endpoint, data=None, headers=None, params=None):
        """http put method with necessary data
        :param url: api base url
        :param endpoint: api endpoint
        :param data: api payload
        :param headers: api header
        :param params: api query param
        :return:api response
        """

        headers = headers if headers else self.headers
        response = requests.put(f'{url}{self.endpoint_version}{endpoint}', headers=headers, json=data, params=params)
        response.raise_for_status()
        return response.json()

    def patch(self, url, endpoint, data=None, headers=None):
        """http patch method with necessary data
        :param url: api base url
        :param endpoint: api endpoint
        :param data: api payload
        :param headers: api header
        :return:api response
        """

        headers = headers if headers else self.headers
        response = requests.patch(f'{url}{self.endpoint_version}{endpoint}', headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, url, endpoint, data=None, headers=None):
        """http delete method with necessary data
        :param url: api base url
        :param endpoint: api endpoint
        :param data: api payload
        :param headers: api header
        :return:api response
        """

        headers = headers if headers else self.headers
        response = requests.delete(f'{url}{self.endpoint_version}{endpoint}', headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def refresh_token(self):
        """
        :return:
        """

        self.token = self.get_token()
        self.headers['Authorization'] = f'Bearer {self.token["access_token"]}'
