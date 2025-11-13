import os
import json
import telebot
from google import genai
from google.genai import types

# Try to import functions_framework (only available in GCF environment)
# Check for FORCE_POLLING env var to override GCF detection for local testing
FORCE_POLLING = os.environ.get("FORCE_POLLING", "false").lower() == "true"

try:
    # Import functions_framework only if not forcing polling
    if not FORCE_POLLING:
        import functions_framework
        IS_GCF = True
    else:
        IS_GCF = False
except ImportError:
    IS_GCF = False

# Initialize clients
tg_token = os.environ.get("TG_BOT_TOKEN")
gemini_api_key = os.environ.get("GEMINI_API_KEY")

print(f"Initializing bot with token: {tg_token[:20] if tg_token else 'MISSING'}...")
print(f"Initializing Gemini with key: {gemini_api_key[:20] if gemini_api_key else 'MISSING'}...")
print(f"Running in GCF mode: {IS_GCF}")

try:
    bot = telebot.TeleBot(tg_token, parse_mode='HTML') if tg_token else None
    if gemini_api_key:
        gemini_client = genai.Client(api_key=gemini_api_key)
        print("New Gemini Client Initialized.")

except Exception as e:
    print(f"Warning during initialization: {e}")
    bot = None


# ============================================================================
# CUSTOMIZE YOUR SYSTEM PROMPT HERE
# ============================================================================

SYSTEM_PROMPT = """You are an AI assistant.

Your guidelines:
- Default Respond in simple english clear and concise, No fluff
- Also translate default respond into simple iban sarawak language
- Respond in **Telegram HTML syntax**. Use <b> for bold, <i> for italic, and <code> for code. DO NOT use markdown characters like * or _ for formatting."""

# ============================================================================
# End of customization - Don't change below
# ============================================================================


def get_gemini_response(user_message):
    """Get response from Gemini with Google Search grounding for internet access"""
    try:
        print(f"get_gemini_response called with: {user_message[:100]}")
        enhanced_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
        
        # 1. Define the Google Search tool as a Tool object (as per your guide)
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )
        
        # 2. Define the configuration object with the tool list (as per your guide)
        config = types.GenerateContentConfig(
            tools=[grounding_tool]
        )
        
        print("Calling generate_content with Google Search enabled...")
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=enhanced_prompt,
            config=config
        )
        # Non-streaming response, access text directly
        full_response = response.text if hasattr(response, 'text') else ""
        print(f"Full response received: {len(full_response)} chars")
        return full_response if full_response else "No response generated"
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        import traceback
        traceback.print_exc()
        # Fallback to non-search version
        print("Falling back to standard generation without search...")
        try:
            response_fallback = gemini_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=enhanced_prompt
            )
            # Non-streaming response, access text directly
            full_response = response_fallback.text if hasattr(response_fallback, 'text') else ""
            return full_response if full_response else "No response generated"
        except Exception as e2:
            print(f"❌ Fallback also failed: {e2}")
            return f"Error: Unable to generate response"


if IS_GCF:
    # ===== GCF WEBHOOK MODE =====
    @functions_framework.http
    def telegram_webhook(request):
        """Cloud Function HTTP endpoint for Telegram webhook"""
        try:
            print("=" * 60)
            print("WEBHOOK REQUEST RECEIVED")
            print("=" * 60)
            
            request_json = request.get_json()
            print(f"Request JSON: {request_json}")
            
            if not request_json:
                print("⚠️  Empty request body")
                return "OK", 200
            
            print("Parsing Telegram update...")
            update = telebot.types.Update.de_json(request_json)
            print(f"Update object created: {update}")
            
            if not update.message:
                print("⚠️  No message in update")
                return "OK", 200
            
            user_message = update.message.text
            chat_id = update.message.chat.id
            user_id = update.message.from_user.id
            
            print(f"✅ Message received!")
            print(f"   Chat ID: {chat_id}")
            print(f"   User ID: {user_id}")
            print(f"   Message: {user_message}")
            
            if not user_message:
                print("⚠️  Message text is empty")
                return "OK", 200
            
            # Get Gemini response
            print("Calling Gemini API...")
            response_text = get_gemini_response(user_message)
            print(f"✅ Gemini response received")
            print(f"   Response: {response_text[:200]}")
            
            # Send response
            print("Sending response to Telegram...")
            if bot:
                bot.send_message(chat_id, response_text)
                print("✅ Message sent successfully!")
            else:
                print("❌ Bot not initialized!")
            
            print("=" * 60)
            return "OK", 200
        
        except Exception as e:
            print(f"❌ ERROR processing webhook: {e}")
            import traceback
            traceback.print_exc()
            return "ERROR", 500

else:
    # ===== LOCAL POLLING MODE =====
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        """Handle incoming messages in polling mode"""
        try:
            user_message = message.text
            chat_id = message.chat.id
            
            print(f"Polling received message from {chat_id}: {user_message[:50]}")
            
            # Get Gemini response
            response_text = get_gemini_response(user_message)
            print(f"Response: {response_text[:100]}")
            
            # Send response
            bot.send_message(chat_id, response_text)
        
        except Exception as e:
            print(f"Error handling message: {e}")
            bot.send_message(message.chat.id, f"Error: {str(e)}")
    
    print("Starting polling mode...")
    bot.infinity_polling(timeout=30)

