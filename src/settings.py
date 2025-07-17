import logging
import os

from dotenv import load_dotenv

"""
Define constants to use token properly
"""

load_dotenv()  # take environment variables from .env

# Configure logging
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# List of the exchange APIs
API_URLS = ['https://web.paribu.com/initials/ticker/extended', 'https://api.btcturk.com/api/v2/ticker']
