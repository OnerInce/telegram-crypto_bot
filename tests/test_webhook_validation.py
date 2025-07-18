import json
import os
from unittest.mock import patch

import pytest

from src.handler import lambda_handler, validate_webhook_secret


def test_validate_webhook_secret_no_secret_configured():
    """Test that validation passes when no secret is configured"""
    with patch.dict(os.environ, {}, clear=True):
        event = {'headers': {}}
        assert validate_webhook_secret(event) is True


def test_validate_webhook_secret_valid_token():
    """Test that validation passes with correct secret token"""
    secret = "test-secret-token"
    with patch.dict(os.environ, {'TELEGRAM_WEBHOOK_SECRET': secret}):
        event = {'headers': {'x-telegram-bot-api-secret-token': secret}}
        assert validate_webhook_secret(event) is True


def test_validate_webhook_secret_invalid_token():
    """Test that validation fails with incorrect secret token"""
    with patch.dict(os.environ, {'TELEGRAM_WEBHOOK_SECRET': 'correct-secret'}):
        event = {'headers': {'x-telegram-bot-api-secret-token': 'wrong-secret'}}
        assert validate_webhook_secret(event) is False


def test_validate_webhook_secret_missing_header():
    """Test that validation fails when header is missing"""
    with patch.dict(os.environ, {'TELEGRAM_WEBHOOK_SECRET': 'test-secret'}):
        event = {'headers': {}}
        assert validate_webhook_secret(event) is False


def test_lambda_handler_unauthorized():
    """Test that lambda handler returns 401 for invalid secret"""
    with patch.dict(os.environ, {'TELEGRAM_WEBHOOK_SECRET': 'correct-secret'}):
        event = {
            'headers': {'x-telegram-bot-api-secret-token': 'wrong-secret'},
            'body': json.dumps({'message': {'chat': {'id': 123}, 'text': 'test', 'from': {'language_code': 'en'}}}),
        }

        response = lambda_handler(event, {})
        assert response['statusCode'] == 401
        assert 'Invalid webhook secret token' in response['body']
