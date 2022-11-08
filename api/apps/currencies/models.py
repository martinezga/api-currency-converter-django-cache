from django.db import models

from apps.audit.models import AuditModel

STATUS_CHOICES = (
    ('created', 'Created'),
    ('updated', 'Updated'),
    ('error', 'error'),
)


class CurrencyModel(AuditModel):
    code = models.CharField(max_length=16, null=False, blank=False, unique=True, verbose_name='currency code')
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)
    is_enabled = models.BooleanField(default=True)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES,
        default='created',
    )

    class Meta:
        db_table = 'currencies'
        ordering = ['code']
