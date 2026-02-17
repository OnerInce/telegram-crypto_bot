# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Telegram bot that provides real-time cryptocurrency prices from Turkish exchanges (Paribu and BTCTurk). The bot is deployed as an AWS Lambda function using SAM (Serverless Application Model) and responds to user queries with crypto prices in Turkish Lira (TRY), Tether (USDT), and Bitcoin (BTC) pairs.

## Architecture

### Core Components

- **handler.py**: Main Lambda entry point that processes Telegram webhook events
- **get_data.py**: Fetches cryptocurrency data from exchange APIs (Paribu and BTCTurk)
- **utils.py**: Core business logic for message creation and Telegram API communication
- **style_message.py**: Formats bot responses with HTML styling
- **translate.py**: Handles Turkish/English localization based on user language
- **settings.py**: Configuration constants including API URLs

### Data Flow

1. User sends message to Telegram bot
2. Telegram webhook triggers AWS Lambda via API Gateway
3. Lambda processes message and queries exchange APIs
4. Bot formats response with prices and sends back to user

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r src/requirements.txt

# Run tests
make test

# Run all checks (formatting, linting, type checking)
make ci
```

### Individual Quality Checks
```bash
# Format code
make format

# Sort imports
make isort

# Type checking
make type

# Lint code
make lint
```

### AWS SAM Commands
```bash
# Validate SAM template
sam validate

# Build application
sam build

# Deploy to AWS
sam deploy --guided

# Run locally with sample event
sam local invoke CryptoBotFunction -e events/event.json

# Start local API server
sam local start-api --env-vars env.json
```

## Environment Setup

### Required Environment Variables
- `BOT_TOKEN`: Telegram bot token from BotFather
- `CMC_API_KEY`: CoinMarketCap API key (optional, for coin name mapping)

### Configuration Files
- `.env.json`: Environment variables for local SAM testing
- `samconfig.toml`: SAM deployment configuration
- `mypy.ini`: Type checking configuration

## Code Quality Standards

The project uses:
- **Black**: Code formatting with line length 120
- **isort**: Import sorting  
- **mypy**: Type checking
- **flake8**: Linting
- **pytest**: Unit testing

Always run `make ci` before committing changes to ensure code quality.

## Testing

Tests are located in the `tests/` directory and cover:
- API integration tests (`test_apis.py`)
- Message styling tests (`test_style.py`)

Run tests with: `PYTHONPATH=src pytest tests`

## Deployment

The project uses GitHub Actions for CI/CD:
- **LintAndTest.yml**: Runs code quality checks and tests
- **DevDeploy.yml**: Deploys to AWS Lambda

Manual deployment: `sam deploy --guided`