import json
import os

from utils import create_message, send_message


def validate_webhook_secret(event):
    """
    Validate the webhook secret token from Telegram
    Returns True if valid, False otherwise
    """
    expected_secret = os.environ.get('TELEGRAM_WEBHOOK_SECRET')

    if not expected_secret:
        # If no secret is configured, skip validation
        return True

    # Get the secret token from headers
    headers = event.get('headers', {})
    received_secret = headers.get('X-Telegram-Bot-Api-Secret-Token')

    return received_secret == expected_secret


def lambda_handler(event, context):
    # Validate webhook secret token
    if not validate_webhook_secret(event):
        return {'statusCode': 401, 'body': json.dumps({'error': 'Invalid webhook secret token'})}

    message = json.loads(event['body'])

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
