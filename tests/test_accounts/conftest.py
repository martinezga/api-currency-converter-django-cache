from pytest_factoryboy import register

from tests.test_accounts import factories

register(factories.AccountFactory)
