# Generated by Django 3.2.16 on 2022-11-10 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currencymodel',
            name='status',
        ),
    ]