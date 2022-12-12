from django.utils import timezone
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
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

    @extend_schema(
        auth=[],
    )
    def list(self, request):
        response = CustomUtil().response
        description = 'List all active and allowed currencies'
        response['request_detail']['description'] = description

        objs = CurrencyModel.objects.filter(is_enabled=True)
        serializer = CurrencySerializer(objs, many=True)

        response['status_code'] = 200
        response['data'].pop('message')
        response['data']['currencies_count'] = len(serializer.data)
        response['data']['active_currencies'] = serializer.data

        return Response(response, status=response['status_code'])

    @extend_schema(
        auth=[],
    )
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
            # Get list of implemented currencies (including enabled and disabled)
            currencies_all = CurrencyModel.objects.all()

            if currencies_all:
                # Get a list of dict keys
                currencies_available_all_code = currencies_available_all.keys()
                currencies_all_code = [x.code for x in currencies_all]

                # Compare between structures
                for currency_available_code in currencies_available_all_code:
                    # save not implemented ones
                    if currency_available_code not in currencies_all_code:
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

    @extend_schema(
        request=inline_serializer(
            name='CurrenciesCreationInlineSerializer',
            fields={
                'currencies': serializers.ListField(
                    child=serializers.CharField(),
                    default=['USD', 'BRL', ]
                ),
            }
        ),
        responses={
            201: inline_serializer(
                name='Currencies creation - Successfully response',
                fields={
                    'request_detail': serializers.DictField(
                        child=serializers.CharField(),
                        default={
                            'description': 'Add new currencies to allow its use on our API',
                            'request_date_utc': timezone.now()
                        }),
                    'data': serializers.DictField(
                        child=serializers.CharField(),
                        default={
                            'message': 'Created'
                        }),
                    'status_code': serializers.IntegerField(default=201),
                }
            ),
            400: inline_serializer(
                name='Currencies creation - Bad request',
                fields={
                    'request_detail': serializers.DictField(
                        child=serializers.CharField(),
                        default={
                            'description': 'Add new currencies to allow its use on our API',
                            'request_date_utc': timezone.now()
                        }),
                    'data': serializers.DictField(
                        child=serializers.DictField(),
                        default={
                            'message': {
                                'currencies': 'No currencies to add. Verify values exists',
                            }
                        }),
                    'status_code': serializers.IntegerField(default=400),
                }
            ),
            401: inline_serializer(
                name='Unauthorized',
                fields={
                    'detail': serializers.CharField(default='Authentication credentials were not provided'),
                }
            ),
        },
    )
    def create(self, request):
        """Admin resource. Add new currencies to allow its use on our API"""

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
            response['status_code'] = 201
        else:
            response['data']['message'] = serializer.errors

        return Response(response, status=response['status_code'])
