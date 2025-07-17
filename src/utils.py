import datetime
import decimal
import logging
import os
from json.decoder import JSONDecodeError

import requests

from get_data import get_coin_price
from settings import API_URLS
from style_message import style_message
from translate import translate

logger = logging.getLogger(__name__)


def get_json_response(request_url):
    # return json response from request url
    try:
        logger.debug(f"Making API request to: {request_url}")
        r = requests.get(request_url, headers={'User-Agent': 'Mozilla/5.0'})
        r.raise_for_status()
        res = r.json()
        logger.debug(f"Successfully received response from: {request_url}")
        return res
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed for {request_url}: {str(e)}")
        raise


def send_message(text, chat_id):
    try:
        bot_url = f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/"
        url = bot_url + "sendMessage?text={}&chat_id={}&parse_mode=html".format(text, chat_id)

        logger.debug(f"Sending message to chat_id: {chat_id}")
        response = requests.get(url)
        response.raise_for_status()
        logger.debug(f"Message sent successfully to chat_id: {chat_id}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message to chat_id {chat_id}: {str(e)}")
        raise


def create_message(coin_input, lang, user_name):
    coin_symbol = coin_input.upper()
    logger.info(f"Creating message for coin: {coin_symbol}")

    all_parse_results = []
    total_fetched_pair = 0
    name_of_coin = None
    is_coin_name_required = True

    for url in API_URLS:
        try:
            parse_result, coin_name_from_exchange = get_coin_price(url, coin_symbol, is_coin_name_required)
            logger.debug(f"Successfully fetched data from {url} for {coin_symbol}")
        except (
            requests.exceptions.RequestException,
            KeyError,
            JSONDecodeError,
        ) as e:
            logger.warning(f"Failed to fetch data from {url} for {coin_symbol}: {str(e)}")
            continue

        # get name of the coin
        if name_of_coin is None and coin_name_from_exchange is not None:
            name_of_coin = coin_name_from_exchange
            is_coin_name_required = False

        all_parse_results.append(parse_result)
        total_fetched_pair += len(parse_result)

    logger.info(f"Total fetched pairs for {coin_symbol}: {total_fetched_pair}")

    if total_fetched_pair < 1:
        logger.warning(f"No price data found for coin: {coin_symbol}")
        return translate("You have entered an invalid symbol", lang)

    prices = []
    now = datetime.datetime.now()

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

    logger.info(f"Successfully created message for {coin_symbol} with {len(prices)//4} price entries")
    return style_message(lang, coin_symbol, name_of_coin, now, prices, user_name)
