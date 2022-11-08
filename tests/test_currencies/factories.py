import factory

from apps.currencies.models import CurrencyModel
from tests.test_accounts.factories import AccountFactory


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CurrencyModel

    code = factory.Faker('pystr', max_chars=10)
    name = factory.Faker('sentence', nb_words=3)
    creator = factory.SubFactory(AccountFactory)
