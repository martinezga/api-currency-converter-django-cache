from rest_framework import serializers

from apps.exchanges.models import ExchangeRateModel


class ExchangeRateSerializer(serializers.ModelSerializer):
    code = serializers.SlugRelatedField(
        read_only=True,
        slug_field='code'
    )
    creator = serializers.StringRelatedField()
    modifier = serializers.StringRelatedField()

    class Meta:
        model = ExchangeRateModel
        fields = '__all__'
