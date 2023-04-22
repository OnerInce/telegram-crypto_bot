import requests

import utils


def get_coin_name_btcturk(coin_symbol):
    """
    try to get name of the coin from another endpoint of BTCTurk
    """

    btcturk_url = 'https://api.btcturk.com/api/v2/server/exchangeinfo'

    try:
        info = utils.get_json_response(btcturk_url)
    except requests.exceptions.RequestException:
        return ''

    all_coins = info['data']['currencies']

    for coin in all_coins:
        if coin['symbol'] == coin_symbol.upper():
            return coin['name']

    return ''  # return empty if coin name not found


def get_coin_name_paribu(coin_symbol):
    """
    try to get name of the coin from another endpoint of Paribu
    """

    paribu_url = 'https://web.paribu.com/initials/config'

    try:
        info = utils.get_json_response(paribu_url)
    except requests.exceptions.RequestException:
        return ''

    coin_obj = info['payload']['currencies'].get(coin_symbol.lower())

    return coin_obj["name"]


def get_coin_price(api_url, target_coin, is_coin_name_wanted):
    # Get exchange data from APIs
    info = utils.get_json_response(api_url)

    if "paribu" in api_url:
        data = info["payload"]
        coin_name = get_coin_name_paribu(target_coin)

        result_list = []

        for key, value in data.items():
            if target_coin.lower() == key.split("_")[0]:
                price = value["last"]
                change = float(value["percentage"])

                parity = key.split("_")[1]

                if parity.upper() == "TL":
                    parity = "TRY"

                result_dict = {
                    "exchange": "Paribu",
                    "counter": parity.upper(),
                    "price": price,
                    "change": change,
                }
                result_list.append(result_dict)

        return result_list, coin_name

    elif "btcturk" in api_url:
        result_list = []

        for obj in info["data"]:
            base = obj["numeratorSymbol"]
            counter = obj["denominatorSymbol"]

            if base == target_coin:
                price = obj["last"]
                change = obj["dailyPercent"]
                result_dict = {
                    "exchange": "BTCTürk",
                    "counter": counter,
                    "price": price,
                    "change": change,
                }
                result_list.append(result_dict)

        name = None

        # make another request for coin name or not
        if is_coin_name_wanted:
            name = get_coin_name_btcturk(target_coin)

        return result_list, name
