<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/FxL5qM0.jpg" alt="Bot logo"></a>
</p>

<h3 align="center">Turkish Crypto Exchange Bot</h3>

<div align="center">

  ![Status](https://img.shields.io/badge/status-active-success.svg)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

The goal of this Telegram bot is to give the user current price of the cryptocurrencies from Turkish exchanges. 
Bot currently supports 2 biggest Turkish exchanges : *Paribu and BTCTurk.* 
After getting data from exchanges' API, SQLite used for data storing purposes. 
Database is updated in every 30 seconds to avoid a rate-limit from exchanges. 
**Prices are given as Turkish Lira (TRY), Tether (USDT) and BTC pair (BTC)**

## 📝 Table of Contents
+ [Demo / Working](#demo)
+ [How it works](#working)
+ [Usage](#usage)
+ [Test](#test)
+ [What's New](#new)
+ [Future Goals](#goals)
+ [Acknowledgments](#acknowledgement)

## 🎥 Demo / Working <a name = "demo"></a>
<img align="center" src="/pics/demo.gif">

## 💭 How it works <a name = "working"></a>

The bot first starts to fill the database. Content of the database updates in 30 seconds according to exchanges' 
API data if there is a new request from a Telegram user. Then, bot constantly checks for a new message from the user. 
If there is a new message, bot reads the command from the user and if it is a valid coin symbol, 
makes a query to the database and returns the corresponding data to user.

## 🎈 Usage <a name = "usage"></a>

There are two ways to use this bot :

**1. Docker Compose** :whale:

Assuming Docker is already installed, run this command from proejct root directory:

```
docker compose up
```
A docker image will be built using Dockerfile and a container will start using docker-compose.yml. All requirements will install and bot will start.

**2. Python Virtual Environment**

Create a Python virtual environment and activate it:

```
pip3 install --upgrade virtualenv
python3 -m venv env
.\env\Scripts\activate
```

Install required packages:

```
pip install -r requirements.txt
```

Enter the coin symbol without slash or something i.e. "eth" (without quotes, case doesn't matter). And bot replies you with information. Because of some coins are not present in all exchanges, only the exchanges that has specific coin shows up in bot's reply. 

## :video_game: Test <a name = "test"></a>

To test and use this bot on Telegram, please see settings.py. Bot is active on **@python_koin_bot** on Telegram

### Prerequisites

To use this bot, you'll need a Telegram bot Token, and a CoinMarketCap API key to retrieve data from CMC.
These information should be in a .env file on project root directory.

* [CoinMarketCap API](https://pro.coinmarketcap.com/signup/)
* [Telegram Bot Token](https://core.telegram.org/bots#creating-a-new-bot)

## :new: What's New <a name = "new"></a>

- July 2019 
  - Project creation
- March 2021 
  - Switched to python-telegram-bot library for more optimized performance 
  - Removed small and closed exchanges
  - Added USDT and BTC pairs
  - Re-organized response message
  - Changed database structure for faster response times

## :dart: Future Goals <a name = "goals"></a>

* Output in a more organized way. (like a table)
* Implement an algorithm which detects arbitrage opportunities and notifies user.
* Allow user to set a notification alarm for a specific coin.


## 🎉 Acknowledgements <a name = "acknowledgement"></a>
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot/) - Built using
* [Stack Overflow](https://stackoverflow.com/) - For obvious reasons
* [Telegram Bot Doc.](https://core.telegram.org/bots) - To understand basic bot commands and process
* [CoinMarketCap API Doc.](https://coinmarketcap.com/api/) - Detailed information to use CMC API
