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

To run the bot in local polling mode, run this command in your terminal:
```bash
export FORCE_POLLING=true
python main.py
```

## How It Works

- **Local Development**: When you run `python main.py`, the `python-dotenv` package automatically loads variables from your `.env` file.
- **Cloud Deployment**: The `deploy_cloud.sh` script reads `TG_KEY` and `GEMINI_KEY` from your local `.env` file and sets them as environment variables in the Google Cloud Function.
- **Security**: The `.env` file is gitignored and should never be committed to version control.

## Cloud Environment Note

**Important:** The deployment script reads the `GEMINI_KEY` from your `.env` file but sets it as `GOOGLE_API_KEY` in the cloud environment. The Python code (`main.py`) is written to read `GOOGLE_API_KEY`, ensuring consistency with the deployed environment and industry standards. This is a critical detail for understanding how the deployed application is configured.

## Files

- `.env` - Your actual credentials (gitignored, never commit this!)
- `.env.example` - Template showing the required format (safe to commit)
- `requirements.txt` - Includes `python-dotenv` package

## Migration from Old Setup

If you previously used `TG_KEY` and `GEM_KEY` files, they have been replaced with the `.env` approach. The new setup is more standardized and follows Python best practices.
