import requests

from src.settings import API_URLS
from src.cmc_data import get_coin_name_mappings


def test_cmc_api():
    coin_name_dict = get_coin_name_mappings()

    assert type(coin_name_dict) == dict
    assert len(coin_name_dict) > 1000


def test_exchange_apis():
    for api in API_URLS:
        r = requests.get(api)

        assert r.status_code == 200
        assert type(r.json()) == dict
