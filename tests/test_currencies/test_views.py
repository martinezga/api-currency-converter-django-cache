import json

import pytest

from tests.test_currencies.factories import CurrencyFactory

pytestmark = pytest.mark.django_db
API_VERSION = '/v1'


class TestCurrencyViews:
    endpoint = f'{API_VERSION}/currencies/'

    def test_list(self, api_client):
        obj_expected = 5
        CurrencyFactory.build_batch(obj_expected)

        response = api_client().get(
            self.endpoint,
        )
        objs_received = json.loads(response.content).get('data').get('active_currencies')

        assert response.status_code == 200
        assert len(objs_received) == obj_expected
