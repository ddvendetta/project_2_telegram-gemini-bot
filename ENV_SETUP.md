# Environment Variables Setup

This project uses **python-dotenv** for secure credential management following best practices.

## Quick Start

### 1. Create your `.env` file

Copy the example file and add your credentials:

```bash
cp .env.example .env
```

Then edit `.env` and add your actual API keys:

```env
# Telegram Bot Configuration
TG_KEY=your_actual_telegram_bot_token_here

# Google Gemini API Configuration
GEMINI_KEY=your_actual_gemini_api_key_here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
./run_local.sh
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TG_KEY` | Telegram Bot Token from @BotFather | `123456789:ABCdefGHIjkl...` |
| `GEMINI_KEY` | Google Gemini API Key | `AIzaSy...` |

## How It Works

- **Local Development**: The `python-dotenv` package automatically loads variables from `.env` file
- **Cloud Deployment**: The `deploy_cloud.sh` script reads from `.env` and sets them as GCP environment variables
- **Security**: The `.env` file is gitignored and never committed to version control

## Files

- `.env` - Your actual credentials (gitignored, never commit this!)
- `.env.example` - Template showing the required format (safe to commit)
- `requirements.txt` - Includes `python-dotenv` package

## Migration from Old Setup

If you previously used `TG_KEY` and `GEM_KEY` files, they have been replaced with the `.env` approach. The new setup is more standardized and follows Python best practices.
