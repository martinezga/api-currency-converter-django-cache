from datetime import datetime

from django.apps import apps
from django.db import models

from apps.audit.models import AuditModel
from apps.utils.exchange_api import GetExchange


class CurrencyModel(AuditModel):
    code = models.CharField(max_length=16, null=False, blank=False, unique=True, verbose_name='currency code')
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'currencies'
        ordering = ['code']

    def create_currency_rate(self):
        ExchangeRModel = apps.get_model('exchanges.ExchangeRateModel')
        # Get exchange rate
        exchange_api = GetExchange()
        exchange_rate = exchange_api.get_exchange_rates()
        if exchange_rate:
            base = exchange_rate['base']
            rate = exchange_rate['rates'].get(self.code)

            # Save exchange rate
            exchange_rate = ExchangeRModel.objects.create(
                code_id=self.id,
                base=base,
                rate=rate,
                last_update_rate=datetime.now(tz=self.created.tzinfo),
                creator_id=self.creator.id,
            )
        else:
            # Save record without rate and status error
            exchange_rate = ExchangeRModel.objects.create(
                code_id=self.id,
                base='unknown',
                rate=0,
                status='error',
                last_update_rate=datetime.now(tz=self.created.tzinfo),
                creator_id=self.creator.id,
            )
        return exchange_rate
