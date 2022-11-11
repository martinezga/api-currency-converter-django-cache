from datetime import datetime

from decouple import config
from django.apps import AppConfig


def update_exchange_rates():
    from apps.exchanges.models import ExchangeRateModel
    from apps.utils.exchange_api import GetExchange
    exchange_api = GetExchange()
    exchange_available = exchange_api.get_exchange_rates()
    if exchange_available:
        # Get list of implemented enabled exchange
        exchange_implemented = ExchangeRateModel.objects.filter(is_enabled=True)

        if exchange_implemented:
            for exchange_saved in exchange_implemented:
                new_rate = exchange_available['rates'].get(exchange_saved.code.code)
                # Check if new rate exist and is not a string
                if new_rate and not isinstance(new_rate, str):
                    exchange_saved.rate = new_rate
                    exchange_saved.last_update_rate = datetime.now(tz=exchange_saved.created.tzinfo)
                    exchange_saved.status = 'updated'
                    exchange_saved.save()


class ExchangesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.exchanges'

    def ready(self):
        # RUN_MAIN check to avoid running the code twice since manage.py runserver runs 'ready' twice on startup
        if config('RUN_MAIN', None) != 'true':
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
            from django.conf import settings

            CRON = settings.CRON_UPDATE_RATES

            if CRON:
                sched = BackgroundScheduler()
                sched.add_job(update_exchange_rates, CronTrigger.from_crontab(CRON))
                sched.start()
