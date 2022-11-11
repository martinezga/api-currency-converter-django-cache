import datetime

from rest_framework.permissions import AllowAny, IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class HomeView(ViewSet):
    permission_classes = [AllowAny]

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
