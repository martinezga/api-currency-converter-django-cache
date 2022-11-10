import requests
from decouple import config


class GetExchange:
    def __init__(self, **kwargs):
        self.url_base = 'https://openexchangerates.org/api'
        self.headers = {'accept': 'application/json'}
        self.api_key = config('EXCHANGE_API_KEY')

    def get_exchange_rates(self):
        endpoint = '/latest.json'
        query_params = 'show_alternative=true'
        url = f'{self.url_base}{endpoint}?{query_params}&app_id={self.api_key}'
        exchange_rates = {}
        # Improvement: save in cache
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            exchange_rates = response.json()

        return exchange_rates

    def get_currencies(self):
        endpoint = '/currencies.json'
        # Improvement: show_inactive=true and compare with our data. We can create our historical
        query_params = 'show_alternative=true&show_inactive=false'
        url = f'{self.url_base}{endpoint}?{query_params}&app_id={self.api_key}'
        currencies = {}
        # Improvement: save in cache
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            currencies = response.json()

        return currencies
