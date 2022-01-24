import json
import os
import sys

from utils import create_message, send_message

sys.path.append(os.path.join(os.path.dirname(__file__)))


def lambda_handler(event, context):
    message = json.loads(event['body'])

    # for testing
    # message = event["result"][0]

    chat_id = message['message']['chat']['id']
    user_text = message['message']['text']

    if user_text == '/start':
        send_message('Hi! Welcome to Bot. You can use /help', chat_id)
        return {'statusCode': 200}

    elif user_text == '/help':
        send_message(
            'Simply just type a coin name e.g. btc, eth, dot. Bot is case-insensitive',
            chat_id,
        )
        return {'statusCode': 200}

    name = message['message']['chat']['first_name']

    message_lang = message['message']['from']['language_code']

    reply = create_message(user_text, message_lang, name)
    send_message(reply, chat_id)

    return {'statusCode': 200, 'body': reply}
