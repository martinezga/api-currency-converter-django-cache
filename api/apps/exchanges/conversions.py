from decimal import Decimal, getcontext

from django.conf import settings
from django.core.cache import cache

from apps.exchanges.models import ExchangeRateModel

# For cache timeout
CACHE_TTL = settings.CACHE_TTL


class ConvertCurrency:

    def convert_currency(self, amount, from_obj, to_obj):
        conversion_ratio = f'{to_obj.code.code}/{from_obj.code.code}'

        conversion_rate = cache.get(conversion_ratio)
        if not conversion_rate:
            getcontext().prec = 9
            conversion_rate = Decimal(to_obj.rate) / Decimal(from_obj.rate)
            # Save in cache
            cache.set(conversion_ratio, conversion_rate, timeout=CACHE_TTL)

        return Decimal(amount) * Decimal(conversion_rate)

    def convert_one_to_other(self, amount, from_obj, to_obj='all', base='USD'):
        allowed_conversion = {}

        if to_obj == 'all':
            exchange_rates = ExchangeRateModel.objects.filter(
                is_enabled=True,
                base=base,
            )
            for exchange_obj in exchange_rates:
                conversion_amount = self.convert_currency(amount, from_obj, exchange_obj)
                conversion_amount = conversion_amount.quantize(Decimal('0.001'))
                allowed_conversion[exchange_obj.code.code] = f'{conversion_amount}'
        else:
            conversion_amount = self.convert_currency(amount, from_obj, to_obj)
            allowed_conversion[to_obj.code] = conversion_amount

        return allowed_conversion
