import os

from dotenv import load_dotenv

"""
Define constants to use token properly
"""

load_dotenv()  # take environment variables from .env


# List of the exchange APIs
API_URLS = ['https://web.paribu.com/initials/ticker/extended', 'https://api.btcturk.com/api/v2/ticker']

# CoinMarketCap API KEY
CMC_API_KEY = os.environ["CMC_KEY"]
