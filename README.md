# Simple Telegram Bot with Gemini AI

A lightweight Telegram bot powered by Google Gemini API, following Python best practices with dotenv for secure credential management.

## Features

- 🤖 Telegram bot integration with pyTelegramBotAPI
- 🧠 Google Gemini AI responses with internet search grounding
- 🔒 Secure credential management with python-dotenv
- 📝 Automatic message chunking for long responses
- 🌐 Dual mode: Local polling & Google Cloud Functions webhook
- 👤 Personalized responses with user name recognition

## Quick Start (Local Development)

### 1. Set up environment variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# Telegram Bot Configuration
TG_KEY=your_telegram_bot_token_here

# Google Gemini API Configuration
GEMINI_KEY=your_gemini_api_key_here
```

**Get your credentials:**
- **Telegram Bot Token**: Chat with [@BotFather](https://t.me/botfather) on Telegram
- **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/apikey)

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the bot locally

```bash
./run_local.sh
```

Or manually:
```bash
export FORCE_POLLING=true
python main.py
```

## Customization

Edit the `SYSTEM_PROMPT` in `main.py` to customize the bot's behavior:

```python
SYSTEM_PROMPT = """You are an AI assistant.

Your guidelines:
- If the user's name is provided, acknowledge them personally
- Respond in simple, clear, and concise English - No fluff
- Also translate default response into simple Iban Sarawak language
- Respond in **Telegram HTML syntax**. Use <b> for bold, <i> for italic, and <code> for code."""
```

## Gemini Integration

The core logic for interacting with the Gemini API is in `main.py`. The final, stable implementation uses the modern `google-genai` library.

Google Search grounding is explicitly enabled using the `config` parameter, which requires importing `types` from the library. This was the key to fixing the tool-related errors.

```python
# main.py snippet

# Add the necessary import at the top of the file
from google.genai import types

# ...

# The final, working API call inside the get_gemini_response function
def get_gemini_response(chat_id, user_message):
    # ...
    client = genai.Client(api_key=gemini_api_key)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=enhanced_prompt,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    google_search=types.GoogleSearch()
                )
            ]
        )
    )
    # ...
```

## How It Works

1. User sends a message to the bot on Telegram
2. Bot receives the message and prepends the user's name for personalization
3. Message is sent to Gemini API with your custom system prompt
4. Gemini processes with Google Search grounding (internet access) and returns a response
5. Response is automatically chunked if over 700 characters
6. Bot sends the response(s) back to the user in HTML format

## Architecture

### System Flow

The bot operates in two modes: **Polling Mode** (local testing) and **Webhook Mode** (cloud deployment).

#### Webhook Mode (Google Cloud Functions)

![Telegram Bot Architecture](telegram_bot_architecture_lr.png)

**Flow:**
1. User sends message via Telegram app
2. Telegram API receives and forwards to GCP webhook
3. Cloud Function processes message and calls Gemini API
4. Gemini API returns AI-generated response
5. Response flows back through the webhook to Telegram API
6. User receives the response

#### Linear Flow Diagram

![Linear Flow](telegram_bot_linear.png)

This simplified view shows the one-way message flow from user to AI response.

### Generate Architecture Diagrams

The project includes a diagram generator using the [Diagrams](https://diagrams.mingrammer.com/) library:

```bash
python generate_diagram.py
```

This creates three visualization variants:
- `telegram_bot_architecture.png` - Top-to-bottom architecture view
- `telegram_bot_architecture_lr.png` - Left-to-right architecture view  
- `telegram_bot_linear.png` - Simplified linear flow

The diagrams feature:
- 🎨 Dark theme matching GitHub's dark mode
- 🏗️ Cloud platform clustering (Google Cloud Platform)
- 🔄 Bidirectional flow visualization
- 🎯 Clear component relationships

## Project Structure

```
.
├── main.py                          # Main application code for the bot
├── deploy_cloud.sh                  # Deployment script for Google Cloud Functions
├── requirements.txt                 # Python dependencies
├── .env.example                     # Example environment file
├── .gitignore                       # Files and directories ignored by Git
├── generate_diagram.py              # Script to generate architecture diagrams
├── ENV_SETUP.md                     # Guide for environment setup
├── PROJECT_STRUCTURE.md             # Detailed project structure document
├── README.md                        # This file
├── *.png                            # Diagram images
└── archive/                         # Contains old and deprecated files
```

## Deployment Options

### Google Cloud Functions (Webhook Mode)

Deploy to GCP for serverless, scalable operation:

```bash
./deploy_cloud.sh YOUR_PROJECT_ID REGION
```

Example:
```bash
./deploy_cloud.sh my-telegram-bot asia-southeast1
```

The script will:
- Read credentials from `.env` file
- Deploy to Google Cloud Functions
- Set up the Telegram webhook automatically

**See `deploy_cloud.sh` for detailed deployment options.**

### Other Platforms

For Railway, Heroku, or VPS deployment, set these environment variables:

| Variable | Description |
|----------|-------------|
| `TG_KEY` | Your Telegram bot token |
| `GEMINI_KEY` | Your Google Gemini API key |

## Environment Variables

The bot uses **python-dotenv** for secure credential management during local development.

### `.env` file
Create a `.env` file for your local environment with the following content:
```env
TG_KEY=your_telegram_bot_token
GEMINI_KEY=your_gemini_api_key
```

### Cloud Deployment Key Management
The `deploy_cloud.sh` script reads these values from your local `.env` file and correctly configures the Google Cloud Function's environment variables.

**Important:** The deployment script reads `GEMINI_KEY` from `.env` but sets it as `GOOGLE_API_KEY` in the cloud environment. The Python code (`main.py`) is written to read `GOOGLE_API_KEY` to ensure it works correctly when deployed.

## Development

### Running in Polling Mode (Local Testing)

Set `FORCE_POLLING=true` to test locally without webhooks:

```bash
export FORCE_POLLING=true
python main.py
```

### Running in Webhook Mode (GCF)

Automatically detected when deployed to Google Cloud Functions.

### Visualization Tools

Generate or regenerate architecture diagrams:

```bash
python generate_diagram.py
```

**Diagram customization** in `generate_diagram.py`:
- Modify `graph_attr` dict to change colors and layout
- Adjust `nodesep` and `ranksep` for spacing
- Change `bgcolor` for different themes
- Add/remove components to match your architecture

The script uses the `diagrams` library which requires Graphviz:
```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz
```

## Message Chunking

Long responses are automatically split into chunks of 700 characters (configurable via `MAX_CHUNK_LIMIT` in `main.py`) to comply with Telegram's limits while maintaining readability.

## Security Best Practices

✅ Uses `.env` file for credentials (gitignored)  
✅ Never commit API keys to version control  
✅ Template file (`.env.example`) shows required format  
✅ Follows python-dotenv standard practices  

## Requirements

### Python Dependencies
- Python 3.12+
- pyTelegramBotAPI
- google-genai
- python-dotenv
- functions-framework (for GCF deployment)
- diagrams (for architecture visualization)

### System Dependencies
- Graphviz (for diagram generation)

## License

This project is open source and available for personal and commercial use.
