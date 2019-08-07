from urllib.request import Request, urlopen
from cmc_data import symbol_dict
from translate import translate
from apis import api_url_list
from bot import TOKEN
import json
import sqlite3
import datetime
import pandas as pd
import requests
import time
				
conn = sqlite3.connect('coindb.sqlite')
cur = conn.cursor()

db_refresh_count = 0

if len(TOKEN) != 45:
	exit()

URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def create_db():

	cur.execute('DROP TABLE IF EXISTS Prices')

	cur.execute('''
	CREATE TABLE IF NOT EXISTS Prices (Time DATE, Coin TEXT, Exchange TEXT, Price INTEGER, Change FLOAT)''')


def get_json_from_url(url):
	# Return parsed json content of the url
	
	response = requests.get(url)
	content = response.content.decode("utf8")
	js = json.loads(content)
    
	return js


def get_updates(update_id):
	# Return json content of the latest update's link
	
	if not update_id is None:
		url = URL + "getUpdates?offset=" + str(update_id)
	else:
		url = URL + "getUpdates"
	js = get_json_from_url(url)
	
	return js


def get_last_chat_id_and_text(updates):
	# Get last message sender's information
	
	num_updates = len(updates["result"])
	last_update = num_updates - 1
	chat_id = updates["result"][last_update]["message"]["chat"]["id"]
	name = updates["result"][last_update]["message"]["chat"]["first_name"]
	language = updates["result"][last_update]["message"]["from"]["language_code"]
	last_update_id = updates["result"][last_update]["update_id"]
	
	greeting = translate("Merhaba ", language) + name.capitalize() + "\n"
		
	# if user enters a non-text -invalid- message
	
	try:
		text = updates["result"][last_update]["message"]["text"]
	except:
		return (-1, chat_id, last_update_id, greeting, language)

		
	return (text, chat_id, last_update_id, greeting, language)


def send_message(text, chat_ID):
	url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_ID)
	requests.get(url)


def create_message(db_refresh_count):
	last_textchat = (None, None, None, None, None)
	update_id = None
	
	while True:

		text, chat, update_id, greeting, language = get_last_chat_id_and_text(get_updates(update_id))

		# if user had entered an invalid message
		
		if text == -1 and (text, chat, update_id, greeting, language) != last_textchat: 
			send_message(translate("Gecersiz kisaltma girdiniz", language), chat)
			last_textchat = (-1, chat, update_id, greeting, language)
			continue

		
		if db_refresh_count == 30: # Update db in every 60 seconds
			db_refresh_count = 0
			continue
		
		elif db_refresh_count == 0:
			create_db()
			
			for url in api_url_list:
				http_check = parse_coin_data(url)
				if http_check == -1:
					send_message(translate("Bir hata olustu", language), chat)
					continue
			
			print(pd.read_sql_query("SELECT * FROM Prices", conn)) # Print db to screen
			
		
		if (text, chat, update_id, greeting, language) != last_textchat: # If there is a new message
			
			coin_name = text.upper()
			cur.execute("SELECT Price, Exchange, Change FROM Prices WHERE Coin = ?", (coin_name, ))
			rows = cur.fetchall()
			
			message = greeting
			if len(rows) < 1 :
				message += translate("Gecersiz kisaltma girdiniz", language)
			else:
				message += coin_name + " (" + symbol_dict.get(coin_name, "") + ")" + translate(" Fiyati: ", language) + "\n"
				for r in rows:
					message += str(r[0]) + " " + str(r[1]) + translate(" Degisim(24 saat): %", language) + str(r[2]) + "\n"
			
			send_message(message, chat)
			last_textchat = (text, chat, update_id, greeting, language)
		
		time.sleep(2)
		db_refresh_count = db_refresh_count + 1

def parse_coin_data(api_url):
	# Get exchange data and store in db
	
	now = datetime.datetime.now()
	try:
		req = Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read().decode()
		info = json.loads(webpage)
	except:
		return -1

	if "paribu" in api_url:
		for object in info:
			cur.execute('''INSERT INTO Prices (Time, Coin, Exchange, Price, Change)
					VALUES (?, ?, ?, ?, ?)''',
						(now.strftime('%H:%M:%S'), object[:-3], "Paribu", info[object]["last"], info[object]["percentChange"]))
		conn.commit()
	
	elif "btcturk" in api_url:
		for object in info:
			if object["pair"][-1] == "Y": # TRY
				currency = object["pair"][:-3]
			elif object["pair"][-1] == "T": # USDT
				currency = object["pair"][:-4]
			cur.execute('''INSERT INTO Prices (Time, Coin, Exchange, Price, Change)
						VALUES (?, ?, ?, ?, ?)''',
						(now.strftime('%H:%M:%S'), currency, "BTCTurk", object["last"], object["dailyPercent"]))
		conn.commit()
	
	elif "koineks" in api_url:
		for object in info:
			cur.execute('''INSERT INTO Prices (Time, Coin, Exchange, Price, Change)
							VALUES (?, ?, ?, ?, ?)''',
						(now.strftime('%H:%M:%S'), object, "Koineks", info[object]["current"], info[object]["change_percentage"]))
		conn.commit()
	
	elif "koinim" in api_url:
		for object in info:
			comp_link = "https://koinim.com/api/v1/ticker/" + object
			try:
				ticker_req = Request(comp_link, headers={'User-Agent': 'Mozilla/5.0'})
				webpage_ticker = urlopen(ticker_req).read().decode()
				koinim_info = json.loads(webpage_ticker)
			except:
				return -1
			cur.execute('''INSERT INTO Prices (Time, Coin, Exchange, Price, Change)
								VALUES (?, ?, ?, ?, ?)''',
						(now.strftime('%H:%M:%S'), object[:-4], "Koinim", koinim_info["last_order"], koinim_info["change_rate"]))
		conn.commit()

create_message(db_refresh_count)
