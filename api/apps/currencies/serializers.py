from rest_framework import serializers

from apps.currencies.models import CurrencyModel
from apps.utils.exchange_api import GetExchange


class CurrencySerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    modifier = serializers.StringRelatedField()

    class Meta:
        model = CurrencyModel
        fields = '__all__'


class CurrencyCreateSerializer(serializers.ModelSerializer):
    currencies = serializers.ListField(allow_empty=False, child=serializers.CharField())

    class Meta:
        model = CurrencyModel
        fields = (
            'currencies',
            'creator',
        )

    def validate_currencies(self, values: list):
        validated_values = []
        exchange_api = GetExchange()
        currencies_available = exchange_api.get_currencies()
        if currencies_available:
            currencies_available_code = currencies_available.keys()
        else:
            raise serializers.ValidationError(
                detail='External API error. Try again later.'
            )

        for code in values:
            # Validate if code exist on external API.
            # If it doesn't exist remove from received data
            if currencies_available_code and code in currencies_available_code:
                # Validate if code exist in DB and remove from received data
                code_from_db = CurrencyModel.objects.filter(code=code).first()
                if not code_from_db:
                    validated_values.append((code, currencies_available[code]))

        if not validated_values:
            raise serializers.ValidationError(
                detail='No currencies to add. Verify values exists.'
            )
        return validated_values

    def create(self, validated_data):
        currencies = validated_data.get('currencies')
        creator = validated_data.get('creator')

        for currency in currencies:
            currency = CurrencyModel.objects.create(
                code=currency[0],
                name=currency[1],
                creator_id=creator.id
            )
            currency.create_currency_rate()

        return currencies
