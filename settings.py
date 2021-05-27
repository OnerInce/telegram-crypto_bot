import os
from dotenv import load_dotenv

"""
Define constants to use token properly
"""

load_dotenv()  # take environment variables from .env.

constants = {
    # List of the exchange APIs
    "API_URLS": ['https://www.paribu.com/ticker', 'https://api.btcturk.com/api/v2/ticker'],
    # Telegram bot token
    "BOT_TOKEN": os.environ['BOT_TOKEN'],
    # SQLite database's file name
    "DB_FILE_NAME": "coindb.sqlite",
    # CoinMarketCap API KEY
    "CMC_API_KEY": os.environ['CMC_KEY'],
}
