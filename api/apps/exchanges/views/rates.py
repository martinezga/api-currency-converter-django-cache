from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.utils.custom import CustomUtil


class ExchangeRateView(ViewSet):
    permission_classes = (AllowAny, )

    def list(self, request):
        response = CustomUtil().response
        description = 'List all available exchange rates'
        response['request_detail']['description'] = description

        return Response(response, status=response['status_code'])
