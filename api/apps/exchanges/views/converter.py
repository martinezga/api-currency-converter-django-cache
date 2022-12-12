from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.currencies.models import CurrencyModel
from apps.exchanges.conversions import ConvertCurrency
from apps.exchanges.models import ExchangeRateModel
from apps.utils.custom import CustomUtil


class ConverterView(ViewSet):
    permission_classes = (AllowAny, )

    @extend_schema(
        auth=[],
    )
    @action(detail=False, url_path='(?P<amount>[.\w]+)/(?P<currency_code>\w+)')
    def one_currency_to_all(self, request, amount, currency_code):
        response = CustomUtil().response
        description = 'Convert the amount of the currency specified into all the currencies available'
        response['request_detail']['description'] = description
        # By default, base conversion is in USD
        base = 'USD'
        currency_obj = CurrencyModel.objects.filter(
            is_enabled=True,
            code=currency_code,
        ).first()
        if currency_obj:
            if currency_code == 'BRL':
                exchange_rate_obj = ExchangeRateModel.objects.filter(
                    is_enabled=True,
                    base=base,
                    code=currency_obj.id).first()
                convert = ConvertCurrency()
                conversion_amounts = convert.convert_one_to_other(amount, from_obj=exchange_rate_obj)

                response['status_code'] = 200
                response['data']['message'] = f'Converted {amount} {currency_code} to other currencies'
                response['data']['conversion_count'] = len(conversion_amounts)
                response['data']['conversion'] = conversion_amounts
            else:
                response['data']['message'] = f'{currency_code} conversion is not implemented yet'
        else:
            response['data']['message'] = 'Not found'
            response['status_code'] = 404

        return Response(response, status=response['status_code'])

    # def any_currency_to_other(self, request):
        # Convert any money value from one currency to another
