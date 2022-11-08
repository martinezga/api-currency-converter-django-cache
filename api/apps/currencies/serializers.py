from rest_framework import serializers

from apps.currencies.models import CurrencyModel


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyModel
        fields = '__all__'
