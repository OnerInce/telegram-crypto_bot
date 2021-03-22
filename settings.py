"""
Define constants to use token properly
"""

constants = {
    # List of the exchange APIs
    "API_URLS": ['https://www.paribu.com/ticker', 'https://api.btcturk.com/api/v2/ticker'],
    # Telegram bot token
    "BOT_TOKEN": "",
    # SQLite database's file name
    "DB_FILE_NAME": "",
    # CoinMarketCap API KEY
    "CMC_API_KEY": '',
}

try:
    from local_settings import constants
except ImportError:
    pass
