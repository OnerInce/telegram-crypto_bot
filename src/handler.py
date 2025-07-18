import json
import logging
import os

from utils import create_message, send_message

logger = logging.getLogger(__name__)


def validate_webhook_secret(event):
    """
    Validate the webhook secret token from Telegram
    Returns True if valid, False otherwise
    """
    expected_secret = os.environ.get('TELEGRAM_WEBHOOK_SECRET')

    if not expected_secret:
        # If no secret is configured, skip validation
        logger.debug("No webhook secret configured, skipping validation")
        return True

    # Get the secret token from headers
    headers = event.get('headers', {})
    received_secret = headers.get('x-telegram-bot-api-secret-token')

    is_valid = received_secret == expected_secret
    if not is_valid:
        logger.warning("Invalid webhook secret token received")
    else:
        logger.debug("Webhook secret validation successful")

    return is_valid


def lambda_handler(event, context):
    try:
        logger.info("Processing webhook request")

        # Validate webhook secret token
        if not validate_webhook_secret(event):
            logger.warning("Webhook validation failed, returning 401")
            return {'statusCode': 401, 'body': json.dumps({'error': 'Invalid webhook secret token'})}

        message = json.loads(event['body'])
        chat_id = message['message']['chat']['id']
        user_text = message['message']['text']

        logger.info(
            f"Processing message from chat_id: {chat_id}, command: {user_text}")

        if user_text == '/start':
            send_message('Hi! Welcome to Bot. You can use /help', chat_id)
            logger.info(f"Sent /start response to chat_id: {chat_id}")
            return {'statusCode': 200}

        elif user_text == '/help':
            send_message(
                'Simply just type a coin name e.g. btc, eth, dot. Bot is case-insensitive',
                chat_id,
            )
            logger.info(f"Sent /help response to chat_id: {chat_id}")
            return {'statusCode': 200}

        name = message['message']['chat']['first_name']
        message_lang = message['message']['from']['language_code']

        logger.info(
            f"Processing crypto query for coin: {user_text}, user: {name}")
        reply = create_message(user_text, message_lang, name)
        send_message(reply, chat_id)
        logger.info(f"Successfully sent crypto data to chat_id: {chat_id}")

        return {'statusCode': 200, 'body': reply}

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return {'statusCode': 500, 'body': json.dumps({'error': 'Internal server error'})}
