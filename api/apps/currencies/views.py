from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.currencies.models import CurrencyModel
from apps.currencies.serializers import CurrencySerializer
from apps.utils.custom import CustomUtil


class CurrencyView(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        response = CustomUtil().response
        description = 'List all active and allowed currencies'
        response['request_detail']['description'] = description

        objs = CurrencyModel.objects.filter(is_enabled=True)
        serializer = CurrencySerializer(objs, many=True)

        response['status_code'] = 200
        response['data'].pop('message')
        response['data']['active_currencies'] = serializer.data
        response['data']['currencies_count'] = len(serializer.data)

        return Response(response, status=response['status_code'])
