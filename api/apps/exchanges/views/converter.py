from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.utils.custom import CustomUtil


class ConverterView(ViewSet):
    permission_classes = (AllowAny, )

    @action(detail=False, url_path='(?P<amount>\w+)/(?P<currency_code>\w+)')
    def one_currency_to_all(self, request, amount, currency_code):
        response = CustomUtil().response
        description = 'Convert the amount of the currency specified into all the currencies available'
        response['request_detail']['description'] = description

        return Response(response, status=response['status_code'])

    # def any_currency_to_other(self, request):
        # Convert any money value from one currency to another
