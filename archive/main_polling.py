import telebot
import os
from google import genai
from google.genai import types

# Initialize Telegram Bot
tg_token = os.environ.get("TG_BOT_TOKEN")
if not tg_token:
    raise ValueError("TG_BOT_TOKEN environment variable not set.")

bot = telebot.TeleBot(tg_token, parse_mode=None)

# Initialize Gemini Client
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

gemini_client = genai.Client(api_key=gemini_api_key)


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


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm a Gemini AI bot. Send me any message and I'll respond.")


def format_gemini_response(response_text):
    """Return response as-is."""
    if not response_text:
        return "No response received."
    return response_text


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    """Handle all messages."""
    bot.send_chat_action(message.chat.id, 'typing')
    
    response = get_gemini_response(message.text)
    formatted_response = format_gemini_response(response)
    
    # Split long messages (Telegram 4096 char limit)
    max_length = 4096
    if len(formatted_response) > max_length:
        chunks = [formatted_response[i:i+max_length] for i in range(0, len(formatted_response), max_length)]
        for chunk in chunks:
            bot.reply_to(message, chunk)
    else:
        bot.reply_to(message, formatted_response)


if __name__ == "__main__":
    print("Bot is running... Press Ctrl+C to stop.")
    bot.infinity_polling()