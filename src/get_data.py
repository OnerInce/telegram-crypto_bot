from utils import get_json_response


def get_coin_name_btcturk(coin_symbol):
    """
    try to get name of the coin from another endpoint of BTCTurk
    """

    btcturk_url = 'https://api.btcturk.com/api/v2/server/exchangeinfo'

    info = get_json_response(btcturk_url)

    all_coins = info['data']['currencies']

    for coin in all_coins:
        if coin['symbol'] == coin_symbol.upper():
            return coin['name']

    return ''  # return empty if coin name not found


def get_coin_price(api_url, target_coin, is_coin_name_wanted):
    # Get exchange data from APIs

    info = get_json_response(api_url)

    if "paribu" in api_url:
        coin_name = info["data"]["currencies"][target_coin.lower()]["name"]

        result_list = []

        for obj in info["data"]["ticker"]:
            pair_name_split = obj.split("-")
            base, counter = (
                pair_name_split[0],
                pair_name_split[1].upper(),
            )

            if base.upper() == target_coin:
                price = info["data"]["ticker"][obj]["c"]
                change = info["data"]["ticker"][obj]["p"]

                if counter == "TL":
                    counter = "TRY"

                result_dict = {
                    "exchange": "Paribu",
                    "counter": counter,
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
