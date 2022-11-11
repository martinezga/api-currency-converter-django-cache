import requests
from decouple import config
from django.conf import settings
from django.core.cache import cache

# For cache timeout
CACHE_TTL = settings.CACHE_TTL


class GetExchange:
    def __init__(self, **kwargs):
        self.url_base = 'https://openexchangerates.org/api'
        self.headers = {'accept': 'application/json'}
        self.api_key = config('EXCHANGE_API_KEY')

    def make_request(self, url, headers=None):
        response = {}
        if not headers:
            headers = self.headers

        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            response = r.json()

        return response

    def get_exchange_rates(self):
        endpoint = '/latest.json'
        query_params = 'show_alternative=true'
        url = f'{self.url_base}{endpoint}?{query_params}&app_id={self.api_key}'
        # Check if exist on cache
        exchange_rates = cache.get(endpoint)
        if not exchange_rates:
            exchange_rates = self.make_request(url)
            # Save it to cache
            cache.set(endpoint, exchange_rates, timeout=CACHE_TTL)

        return exchange_rates

    def get_currencies(self):
        endpoint = '/currencies.json'
        # Improvement: show_inactive=true and compare with our data. We can create our historical
        query_params = 'show_alternative=true&show_inactive=false'
        url = f'{self.url_base}{endpoint}?{query_params}&app_id={self.api_key}'
        # Check if exist on cache
        currencies = cache.get(endpoint)
        if not currencies:
            currencies = self.make_request(url)
            # Save it to cache
            cache.set(endpoint, currencies, timeout=CACHE_TTL)

        return currencies
