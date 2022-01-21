import json

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from src.settings import CMC_API_KEY


def get_coin_name_mappings():
    """
    returns a dict of coin_symbol-coin_name mappings e.g. {BTC:Bitcoin}
    """

    # Create dict to map coin names with symbols
    symbol_dict = dict()

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {'start': '1', 'limit': '2000', 'convert': 'USD'}
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY,  # Enter your API key here
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        for obj in data["data"]:
            coin_name = obj["name"]
            coin_symbol = obj["symbol"]
            symbol_dict[coin_name] = coin_symbol

    except (ConnectionError, Timeout, TooManyRedirects):
        return {}

    # Reverse symbol_dict
    symbol_dict = {symbol: coin_name for coin_name, symbol in symbol_dict.items()}

    return symbol_dict
