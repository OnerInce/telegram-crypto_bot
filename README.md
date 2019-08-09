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

The goal of this Telegram bot is to give the user current price of the cryptocurrencies from Turkish exchanges. Bot currently supports 4 biggest Turkish exchanges : *Paribu, BTCTurk, Koineks, Koinim.* After getting data from exchanges' API, SQLite used for data storing purposes. Database is updated in every 90 seconds to avoid a rate-limit from exchanges. **Prices are given as Turkish Lira (TRY).**

## 📝 Table of Contents
+ [Demo / Working](#demo)
+ [How it works](#working)
+ [Usage](#usage)
+ [Test](#test)
+ [Future Goals](#goals)
+ [Authors](#authors)
+ [Acknowledgments](#acknowledgement)

## 🎥 Demo / Working <a name = "demo"></a>
<img align="center" src="/pics/demo.gif">

## 💭 How it works <a name = "working"></a>

The bot first starts to fill the database. Content of the database updates in 90 seconds according to exchanges' API data. Then, in every 2 seconds bot checks for a new message from the user. If there is a new message, bot reads the command from the user and if it is a valid coin symbol, makes a query to the database and returns the corresponding data to user.

## 🎈 Usage <a name = "usage"></a>

To use the bot:

Enter the coin symbol without slash or something i.e. "eth" (without quotes, case doesn't matter). And bot replies you with information. Because of some coins are not present in all exchanges, only the exchanges that has specific coin shows up in bot's reply. 

## :video_game: Test <a name = "test"></a>

To test and use this bot on Telegram, please see bot.py. All suggestions are welcome. 

### Prerequisites

To use this bot, you'll need a Python installation, with a proper Telegram bot TOKEN. You'll also need a CoinMarketCap API key to retrieve data from CMC. Also to run this bot constantly, you need a running computer all the time.

* [Python](https://www.python.org/downloads/)
* [CoinMarketCap API](https://pro.coinmarketcap.com/signup/)
* [Telegram Bot Token](https://core.telegram.org/bots#creating-a-new-bot)

## :dart: Future Goals <a name = "goals"></a>

* Output in a more organized way. (like a table)
* Implement an algorithm which detects arbitrage opportunities and notifies user.
* Provide a small, weekly-change graph to user.
* Allow user to set a notification alarm for a specific coin.


## ✍️ Authors <a name = "authors"></a>
+ [@OnerInce](https://github.com/OnerInce) - Idea & all work


## 🎉 Acknowledgements <a name = "acknowledgement"></a>
* [Stack Overflow](https://stackoverflow.com/) - For obvious reasons
* [Telegram Bot Doc.](https://core.telegram.org/bots) - To understand basic bot commands and process
* [CoinMarketCap API Doc.](https://coinmarketcap.com/api/) - Detailed information to use CMC API
