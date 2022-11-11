import factory

from apps.currencies.models import CurrencyModel
from tests.test_accounts.factories import AccountFactory


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CurrencyModel

    class Params:
        currency_full = factory.Faker('currency')

    code = factory.LazyAttribute(lambda o: f'{o.currency_full[0]}')
    name = factory.LazyAttribute(lambda o: f'{o.currency_full[1]}')
    creator = factory.SubFactory(AccountFactory)
