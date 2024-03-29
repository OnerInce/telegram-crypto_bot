import datetime
import decimal
import os

import requests

from get_data import get_coin_price
from settings import API_URLS
from style_message import style_message
from translate import translate

from json.decoder import JSONDecodeError


def get_json_response(request_url):
    # return json response from request url

    r = requests.get(request_url, headers={'User-Agent': 'Mozilla/5.0'})
    res = r.json()

    return res


def send_message(text, chat_id):
    bot_url = f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/"

    url = bot_url + "sendMessage?text={}&chat_id={}&parse_mode=html".format(text, chat_id)
    requests.get(url)


def create_message(coin_input, lang, user_name):
    coin_symbol = coin_input.upper()
    all_parse_results = []

    # fetched number of pair data
    total_fetched_pair = 0

    name_of_coin = None

    # if coin name still unknown, try to get in next request
    is_coin_name_required = True

    for url in API_URLS:
        try:
            parse_result, coin_name_from_exchange = get_coin_price(url, coin_symbol, is_coin_name_required)
        except (requests.exceptions.RequestException, KeyError, JSONDecodeError):  # exchange API unreachable or coin not in exchange
            continue

        # get name of the coin
        if name_of_coin is None and coin_name_from_exchange is not None:
            name_of_coin = coin_name_from_exchange
            is_coin_name_required = False

        all_parse_results.append(parse_result)
        total_fetched_pair += len(parse_result)

    prices = []
    now = datetime.datetime.now()

    if total_fetched_pair < 1:
        return translate("You have entered an invalid symbol", lang)
    else:
        for exchange_result in all_parse_results:  # get each exchange's and pair's data
            for r in exchange_result:
                exchange_name = r["exchange"]
                counter = r["counter"]
                price = r["price"]
                change = r["change"]

                decimal.getcontext().prec = 3
                price_fixed_float = str(decimal.getcontext().create_decimal(price))

                if "e" not in str(price):  # if not scientific notation
                    price_fixed_float = str(float(price_fixed_float))

                price = price_fixed_float
                prices.extend((exchange_name, counter, price, change))

    return style_message(lang, coin_symbol, name_of_coin, now, prices, user_name)
