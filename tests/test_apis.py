import requests
from dotenv import load_dotenv

from src.settings import API_URLS

load_dotenv()


def test_exchange_apis():
    for api in API_URLS:
        r = requests.get(api)

        assert r.status_code == 200
        assert type(r.json()) == dict
