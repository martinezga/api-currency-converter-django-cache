from datetime import date

from django.db import models

from apps.audit.models import AuditModel
from apps.currencies.models import CurrencyModel

STATUS_CHOICES = (
    ('created', 'Created'),
    ('updated', 'Updated'),
    ('error', 'error'),
)


class ExchangeRateModel(AuditModel):
    code = models.ForeignKey(
        CurrencyModel,
        null=False, blank=False,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_code',
    )
    base = models.CharField(max_length=16)
    rate = models.FloatField(null=False, blank=False, default=0)
    is_enabled = models.BooleanField(default=True)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES,
        default='created',
    )
    last_update_rate = models.DateTimeField(default=date(1900, 12, 1))

    class Meta:
        db_table = 'exchange_rates'
        ordering = ['code']
