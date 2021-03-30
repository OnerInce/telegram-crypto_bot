"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.

Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the bot.
"""
import datetime
import logging
import sqlite3
from urllib.request import Request, urlopen
from translate import translate
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from cmc_data import symbol_dict
import decimal
from settings import constants
import pytz

TIME_BETWEEN_REQUESTS = 30  # seconds
LAST_FETCH_TIME = datetime.datetime.min

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def make_bold(text):
    return "<b>" + text + "</b>"


def make_italic(text):
    return "<i>" + text + "</i>"


def make_pre(text):
    return "<code>" + text + "</code>"


def style_message(lang_code, coin, all_prices):
    day = LAST_FETCH_TIME.strftime("%m/%d/%Y")
    time = LAST_FETCH_TIME.strftime("%H:%M:%S")

    message = day + ", " + make_bold(time + " GMT") + "\n"
    message += coin + " (" + symbol_dict.get(coin, "") + ")" + translate(" Price: ", lang_code) + "\n"

    for i in range(0, len(all_prices), 4):
        exchange = all_prices[i]
        parity = all_prices[i + 1]
        price = all_prices[i + 2]
        change = all_prices[i + 3]

        if change[1] == "-":
            change_sym = "-"
        else:
            change_sym = "+"

        if exchange == 'Paribu':
            message += make_pre(exchange) + 3 * " " + "> "
        else:
            message += make_pre(exchange) + " " + "> "

        message += make_bold(price) + " " + make_italic(parity) + " " * 5
        message += change_sym + "%" + change + "\n"
    return message


def create_db():
    conn = sqlite3.connect(constants["DB_FILE_NAME"])
    cur = conn.cursor()

    cur.executescript('''
    DROP TABLE IF EXISTS Pair;
    DROP TABLE IF EXISTS Exchange;
    DROP TABLE IF EXISTS Price;

    CREATE TABLE Pair (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        first TEXT,
        second TEXT
    );

    CREATE TABLE Exchange (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE 
    );

    CREATE TABLE Price (
        Time DATE,
        pair_id INTEGER, 
        exchange_id INTEGER, 
        Price INTEGER, 
        Change FLOAT,
        PRIMARY KEY (pair_id, exchange_id)
    )''')

    conn.close()


def create_message(coin_input, lang, time):
    conn_f = sqlite3.connect(constants["DB_FILE_NAME"])
    cur_f = conn_f.cursor()

    now = datetime.datetime.now().replace(microsecond=0)

    global LAST_FETCH_TIME
    elapsed_time = (now - LAST_FETCH_TIME).total_seconds()

    if elapsed_time > TIME_BETWEEN_REQUESTS:
        for url in constants["API_URLS"]:
            http_check = parse_coin_data(url, time)
            if http_check == -1:
                print("An error has occurred")
                continue

    coin_name = coin_input.upper()

    cur_f.execute("""SELECT first, second, Price, exchange_id, Change FROM Price 
                    JOIN Pair ON Price.pair_id = Pair.id WHERE first = ?""", (coin_name,))
    rows = cur_f.fetchall()

    prices = []

    if len(rows) < 1:
        return translate("You have entered an invalid symbol", lang)
    else:
        for r in rows:  # get each exchange's and pair's data
            cur_f.execute("SELECT name FROM Exchange WHERE id = ?", (r[3],))
            exchange_name = cur_f.fetchone()[0]
            parity = str(r[1])
            change = str(r[4])
            decimal.getcontext().prec = 3
            price_fixed_float = str(decimal.getcontext().create_decimal(r[2]))
            if "e" not in str(r[2]):  # if not scientific notation
                price_fixed_float = str(float(price_fixed_float))
            price = price_fixed_float

            prices.extend((exchange_name, parity, price, change))

    conn_f.close()

    return style_message(lang, coin_name, prices)


def parse_coin_data(api_url, request_time):
    # Get exchange data and store in DB

    conn_g = sqlite3.connect(constants["DB_FILE_NAME"])
    cur_g = conn_g.cursor()

    now = datetime.datetime.now()
    global LAST_FETCH_TIME
    LAST_FETCH_TIME = request_time
    print("Parse coin Data Last Request: ", now)

    try:
        req = Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read().decode()
        info = json.loads(webpage)
    except:
        return -1

    if "paribu" in api_url:
        for object in info:

            pair_name_split = object.split("_")
            first_name, second_name = pair_name_split[0], pair_name_split[1]

            if second_name == "TL":
                second_name = "TRY"

            cur_g.execute('INSERT OR IGNORE INTO Pair (first, second) VALUES (?, ?)', (first_name, second_name,))
            cur_g.execute('SELECT id FROM Pair WHERE first = ? AND second = ?', (first_name, second_name,))
            pair_id = cur_g.fetchone()[0]

            cur_g.execute('INSERT OR IGNORE INTO Exchange (name) VALUES (?)', ("Paribu",))
            cur_g.execute('SELECT id FROM Exchange WHERE name = ? ', ("Paribu",))
            exchange_id = cur_g.fetchone()[0]

            cur_g.execute('''INSERT OR REPLACE INTO Price (Time, pair_id, exchange_id, Price, Change) 
                VALUES (?, ?, ?, ?, ?)''', (
                now.strftime('%H:%M:%S'), pair_id, exchange_id, info[object]["last"], info[object]["percentChange"],))
        conn_g.commit()

    elif "btcturk" in api_url:
        for object in info["data"]:
            first_name = object["numeratorSymbol"]
            second_name = object["denominatorSymbol"]
            price = object["last"]
            change = object["dailyPercent"]

            cur_g.execute('INSERT OR IGNORE INTO Pair (first, second) VALUES (?, ?)', (first_name, second_name,))
            cur_g.execute('SELECT id FROM Pair WHERE first = ? AND second = ?', (first_name, second_name,))
            pair_id = cur_g.fetchone()[0]

            cur_g.execute('INSERT OR IGNORE INTO Exchange (name) VALUES (?)', ("BTCTurk",))
            cur_g.execute('SELECT id FROM Exchange WHERE name = ? ', ("BTCTurk",))
            exchange_id = cur_g.fetchone()[0]

            cur_g.execute('''INSERT OR REPLACE INTO Price (Time, pair_id, exchange_id, Price, Change) 
                VALUES (?, ?, ?, ?, ?)''',
                          (now.strftime('%H:%M:%S'), pair_id, exchange_id, price, change,))

        conn_g.commit()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    start_lang = update["message"].from_user["language_code"]
    start_text = translate('Hi! Welcome to Bot. You can use /help', start_lang)

    update.message.reply_text(start_text)


def help(update, context):
    """Send a message when the command /help is issued."""
    help_lang = update["message"].from_user["language_code"]
    help_text = translate('Simply just type a coin name such as BTC, ETH, DOT. Bot is case-insensitive', help_lang)

    update.message.reply_text(help_text)


def echo(update, context):
    """Echo the coin prices to user."""
    message_lang = update["message"].from_user["language_code"]
    message_time = update["message"]["date"]
    message_time = message_time.replace(tzinfo=None)
    print("MESSAGE TIME: ", message_time)

    reply = create_message(update.message.text, message_lang, message_time)
    update.message.reply_text(reply, parse_mode="HTML")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start_bot():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(constants["BOT_TOKEN"])

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand - fetch coin price
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    create_db()
    start_bot()
