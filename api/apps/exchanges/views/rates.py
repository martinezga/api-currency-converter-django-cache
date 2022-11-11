from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.exchanges.models import ExchangeRateModel
from apps.exchanges.serializers import ExchangeRateSerializer
from apps.utils.custom import CustomUtil


class ExchangeRateView(ViewSet):
    permission_classes = (AllowAny, )

    def list(self, request):
        response = CustomUtil().response
        description = 'List all available exchange rates'
        response['request_detail']['description'] = description

        objs = ExchangeRateModel.objects.filter(is_enabled=True)
        serializer = ExchangeRateSerializer(objs, many=True)

        response['status_code'] = 200
        response['data'].pop('message')
        response['data']['currencies_count'] = len(serializer.data)
        response['data']['currency_rates'] = serializer.data

        return Response(response, status=response['status_code'])
