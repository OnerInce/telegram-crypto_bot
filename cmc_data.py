# Using CoinMarketCap's API, map coin names and symbols

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from settings import constants
import json

# Create dict to map coin names with symbols
symbol_dict = dict()

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '5000',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': constants["CMC_API_KEY"],  # Enter your API key here
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    count = 0

    for object in data["data"]:
        if count == 100: break  # Only get first 100 coins
        coin_name = object["name"]
        coin_symbol = object["symbol"]
        symbol_dict[coin_name] = coin_symbol
        count = count + 1

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

# Reverse symbol_dict  
symbol_dict = {symbol: coin_name for coin_name, symbol in symbol_dict.items()}
