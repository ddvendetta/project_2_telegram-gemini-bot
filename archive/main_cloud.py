import os
import json
import telebot
import google.generativeai as genai

try:
    import functions_framework
except ImportError:
    functions_framework = None

# Initialize clients
tg_token = os.environ.get("TG_BOT_TOKEN")
gemini_api_key = os.environ.get("GEMINI_API_KEY")

print(f"Initializing bot with token: {tg_token[:20] if tg_token else 'MISSING'}...")
print(f"Initializing Gemini with key: {gemini_api_key[:20] if gemini_api_key else 'MISSING'}...")

try:
    bot = telebot.TeleBot(tg_token, parse_mode=None) if tg_token else None
    genai.configure(api_key=gemini_api_key) if gemini_api_key else None
    gemini_client = None  # Not used in the simplified version
except Exception as e:
    print(f"Warning during initialization: {e}")
    bot = None
    gemini_client = None


# ============================================================================
# CUSTOMIZE YOUR SYSTEM PROMPT HERE
# ============================================================================

SYSTEM_PROMPT = """You are an AI assistant.

Your guidelines:
1. Default Respond in simple english clear and concise, No fluff
2. Also translate default respond into simple iban sarawak language
3. For every prompt your get in other languages, translate it into simple english first then follow guideline from 1. """

# ============================================================================
# End of customization - Don't change below
# ============================================================================


def get_gemini_response(user_message):
    """Send message to Gemini with custom system prompt."""
    try:
        enhanced_prompt = f"""{SYSTEM_PROMPT}

User Question: {user_message}

Please provide a helpful response."""

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(enhanced_prompt, stream=True)
        
        response_text = ""
        for chunk in response:
            if chunk.text:
                response_text += chunk.text
        
        return response_text if response_text else "No response received."
    except Exception as e:
        return f"Error: {str(e)}"


def telegram_webhook(request):
    """HTTP Cloud Function for Telegram webhook."""
    try:
        # Get JSON from Telegram
        json_data = request.get_json()
        
        if not json_data:
            return "No data", 200
        
        # Parse update
        update = telebot.types.Update.de_json(json_data)
        
        # Process if it has a message
        if update and update.message and update.message.text:
            chat_id = update.message.chat.id
            user_message = update.message.text
            
            if not bot:
                print("Bot not initialized")
                return "Bot not initialized", 500
            
            # Get response from Gemini
            response = get_gemini_response(user_message)
            
            # Handle long messages (Telegram 4096 char limit)
            max_length = 4096
            if len(response) > max_length:
                chunks = [response[i:i+max_length] for i in range(0, len(response), max_length)]
                for chunk in chunks:
                    bot.send_message(chat_id, chunk)
            else:
                bot.send_message(chat_id, response)
        
        return "OK", 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return "Error", 500


# Apply functions_framework decorator if available
if functions_framework:
    telegram_webhook = functions_framework.http(telegram_webhook)

