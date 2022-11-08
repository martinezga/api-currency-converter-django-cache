from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel


class AuditModel(TimeStampedModel):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)s_creator_user',
        on_delete=models.CASCADE,
    )
    modifier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)s_modifier_user',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        abstract = True
