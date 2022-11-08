from pytest_factoryboy import register

from tests.test_currencies import factories

register(factories.CurrencyFactory)
