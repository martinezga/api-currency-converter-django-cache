# Generated by Django 3.2.16 on 2022-11-10 16:15

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('currencies', '0002_remove_currencymodel_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('base', models.CharField(max_length=16)),
                ('rate', models.FloatField(default=0)),
                ('is_enabled', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('created', 'Created'), ('updated', 'Updated'), ('error', 'error')], default='created', max_length=16)),
                ('last_update_rate', models.DateTimeField(default=datetime.date(1900, 12, 1))),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchanges_exchangeratemodel_code', to='currencies.currencymodel')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchanges_exchangeratemodel_creator_user', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exchanges_exchangeratemodel_modifier_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'exchange_rates',
                'ordering': ['code'],
            },
        ),
    ]
