from decimal import Decimal, getcontext

from apps.exchanges.models import ExchangeRateModel


class ConvertCurrency:

    def convert_currency(self, amount, from_obj, to_obj):
        getcontext().prec = 9
        conversion_rate = Decimal(to_obj.rate) / Decimal(from_obj.rate)
        # Save in cache ratio 'to_code/from_code' = conversion_rate

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
