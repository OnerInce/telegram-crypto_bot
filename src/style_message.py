from .translate import translate


def style_message(lang_code, coin_sym, coin_name, fetch_time, all_prices, user):
    # Create final styled message

    def make_bold(text):
        return "<b>" + str(text) + "</b>"

    def make_italic(text):
        return "<i>" + str(text) + "</i>"

    def make_pre(text):
        return "<code>" + str(text) + "</code>"

    day = fetch_time.strftime("%m/%d/%Y")
    time = fetch_time.strftime("%H:%M:%S")

    message = f'{day}, {make_bold(time + " GMT")}' + "\n"
    message += translate("Hello " + make_italic(user), lang_code) + "\n"
    message += f'{coin_sym} ({coin_name}){translate(" Price: ", lang_code)}' + "\n"

    # iterate through exchange data and create response message

    for i in range(0, len(all_prices), 4):
        exchange = all_prices[i]
        parity = all_prices[i + 1]
        price = all_prices[i + 2]
        change = all_prices[i + 3]

        if change < 0:
            change_sym = "-"
            change = str(change)[1:]
        else:
            change_sym = " "

        if exchange == 'Paribu':
            message += make_pre(exchange) + 3 * " " + "> "
        else:
            message += make_pre(exchange) + " " + "> "

        message += make_bold(price) + " " + make_italic(parity) + " " * 5
        message += change_sym + "%" + str(change) + "\n"

    return message
