from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.currencies.models import CurrencyModel
from apps.currencies.serializers import CurrencySerializer, CurrencyCreateSerializer
from apps.utils.custom import CustomUtil
from apps.utils.exchange_api import GetExchange


class CurrencyView(ViewSet):
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (AllowAny,)
        return [permission() for permission in permission_classes]

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

    @action(detail=False)
    def to_implement(self, request):
        response = CustomUtil().response
        description = 'List currencies available to add it as active'
        response['request_detail']['description'] = description
        currencies_to_implement = {}

        # Get list of all currencies available from the Exchange API
        exchange_api = GetExchange()
        currencies_available_all = exchange_api.get_currencies()
        if currencies_available_all:
            # Get list of our active currencies (already implemented)
            currencies_active = CurrencyModel.objects.all()

            if currencies_active:
                # Get a list of dict keys
                currencies_available_all_code = currencies_available_all.keys()
                currencies_active_code = [x.code for x in currencies_active]

                # Compare between structures
                for currency_available_code in currencies_available_all_code:
                    # save not implemented ones
                    if currency_available_code not in currencies_active_code:
                        currency_name = currencies_available_all.get(currency_available_code)
                        currencies_to_implement[currency_available_code] = currency_name
            else:
                currencies_to_implement = currencies_available_all
            # List all currencies available to implement in our API
            response['data'].pop('message')
            response['data']['currencies_count'] = len(currencies_to_implement)
            response['data']['currencies_available_all'] = currencies_to_implement
            response['status_code'] = 200

        return Response(response, status=response['status_code'])

    def create(self, request):
        """Input: {'currencies': ['code1', 'code2', ... ]}"""

        response = CustomUtil().response
        description = 'Add new currencies to allow its use on our API'
        response['request_detail']['description'] = description
        data = request.data
        user = request.user
        data['creator'] = user.id
        serializer = CurrencyCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            response['data']['message'] = f'Created'
            response['status_code'] = 200
        else:
            response['data']['message'] = serializer.errors

        return Response(response, status=response['status_code'])
