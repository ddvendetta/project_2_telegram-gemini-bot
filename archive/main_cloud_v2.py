import os
import json
import telebot
from google import genai
from google.genai import types
import functions_framework
from flask import Flask, request

# Create Flask app
app = Flask(__name__)

# Initialize clients
tg_token = os.environ.get("TG_BOT_TOKEN")
gemini_api_key = os.environ.get("GEMINI_API_KEY")

print(f"Initializing bot with token: {tg_token[:20] if tg_token else 'MISSING'}...")
print(f"Initializing Gemini with key: {gemini_api_key[:20] if gemini_api_key else 'MISSING'}...")

bot = telebot.TeleBot(tg_token, parse_mode=None) if tg_token else None
gemini_client = genai.Client(api_key=gemini_api_key) if gemini_api_key else None


# ============================================================================
# CUSTOMIZE YOUR SYSTEM PROMPT HERE
# ============================================================================

SYSTEM_PROMPT = """You are an AI assistant.

Your guidelines:
- Respond in simple terms, short and straight to the point
- No fluff
- Structure long responses into paragraphs of 30 words
- For every response translate into simple iban sarawak language
- For every prompt in other languages, translate it and respond in english"""

# ============================================================================
# End of customization - Don't change below
# ============================================================================


def get_gemini_response(user_message):
    """Send message to Gemini with custom system prompt."""
    if not gemini_client:
        return "Gemini client not initialized. Check your API key."
    
    try:
        enhanced_prompt = f"""{SYSTEM_PROMPT}

User Question: {user_message}

Please provide a helpful response."""

        model = "gemini-2.0-flash"
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=enhanced_prompt)],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            response_modalities=["TEXT"],
            temperature=0.7,
        )

        response_text = ""
        for chunk in gemini_client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if (chunk.candidates is None or len(chunk.candidates) == 0 or 
                chunk.candidates[0].content is None or 
                chunk.candidates[0].content.parts is None or 
                len(chunk.candidates[0].content.parts) == 0):
                continue
            
            part = chunk.candidates[0].content.parts[0]
            if hasattr(part, 'text') and part.text:
                response_text += part.text
        
        return response_text if response_text else "No response received."
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/", methods=["POST"])
def telegram_webhook():
    """HTTP endpoint for Telegram webhook."""
    try:
        # Get JSON from request
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


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
