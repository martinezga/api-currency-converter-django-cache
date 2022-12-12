import datetime

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class HomeView(ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
        auth=[],
    )
    def list(self, request):
        """API home"""
        response = {
            'request_detail': {
                'name': 'home',
                'description': 'Currency converter API',
                'request_date_utc': datetime.datetime.utcnow(),
            },
            'data': {
                'message': 'Up and running'
            },
            'status_code': 200,
        }
        return Response(response, status=response['status_code'])
