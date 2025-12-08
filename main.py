import os
import json
import html
import telebot
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
tg_token = os.environ.get("TG_KEY")
gemini_api_key = os.environ.get("GEMINI_KEY")

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
- If the user's name is provided in the prompt (e.g., "Hello [Name], you asked:"), start your response by acknowledging the user, e.g., "Hello [Name]! Here's your response:".
- Default Respond in simple english clear and concise, No fluff
- Also translate default respond into simple iban sarawak language
- Respond in **Telegram HTML syntax**. Use <b> for bold, <i> for italic, and <code> for code. DO NOT use markdown characters like * or _ for formatting."""

# ============================================================================
# End of customization - Don't change below
# ============================================================================

# Define the hard character limit for each chunk (Keep this around 700-4000)
MAX_CHUNK_LIMIT = 700 

def chunk_response_for_telegram(gemini_text):
    """
    Splits the Gemini response into chunks of MAX_CHUNK_LIMIT characters.
    It attempts to find the last newline or space to avoid breaking words/tags.
    
    Returns a list of strings (chunks).
    """
    
    chunks = []
    current_index = 0
    
    while current_index < len(gemini_text):
        # Determine the maximum length for the current chunk
        end_index = min(current_index + MAX_CHUNK_LIMIT, len(gemini_text))
        
        # Check if this is the last chunk
        if end_index == len(gemini_text):
            chunk = gemini_text[current_index:]
        else:
            # Try to find the last space or newline before the limit to avoid breaking a word or tag
            break_point = gemini_text.rfind('\n\n', current_index, end_index)
            if break_point == -1:
                break_point = gemini_text.rfind(' ', current_index, end_index)
            
            # If no good break point is found, break exactly at the limit
            if break_point <= current_index:
                break_point = end_index

            chunk = gemini_text[current_index:break_point]
            end_index = break_point # Update end_index for the next iteration
        
        chunks.append(chunk.strip())
        current_index = end_index
        
    # If the original response was chunked (i.e., multiple messages), 
    # add a final message indicating the end of the full response.
    if len(chunks) > 1:
         # Use the first part of the original response to create a header for clarity
        header = f"<b>Full Response (Part 1/{len(chunks)})</b>\n\n"
        chunks[0] = header + chunks[0]
        
        # Add a footer to the last chunk
        footer = "\n\n<i>[End of full response]</i>"
        chunks[-1] = chunks[-1] + footer
        
    return [c for c in chunks if c] # Filter out any empty strings

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
            model="gemini-2.0-flash-exp",
            contents=enhanced_prompt,
            config=config
        )
        # Non-streaming response, access text directly
        full_response = response.text if hasattr(response, 'text') else ""
        print(f"Full response received: {len(full_response)} chars")
        return full_response if full_response else "No response generated"
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"❌ Gemini error: {error_type}: {error_msg}")
        import traceback
        traceback.print_exc()
        # Fallback to non-search version
        print("Falling back to standard generation without search...")
        try:
            response_fallback = gemini_client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=enhanced_prompt
            )
            # Non-streaming response, access text directly
            full_response = response_fallback.text if hasattr(response_fallback, 'text') else ""
            return full_response if full_response else "No response generated"
        except Exception as e2:
            error_type2 = type(e2).__name__
            error_msg2 = str(e2)
            print(f"❌ Fallback also failed: {error_type2}: {error_msg2}")
            # Return detailed error information with HTML escaping
            detailed_error = f"<b>❌ Gemini API Error</b>\n\n"
            detailed_error += f"<b>Primary Error ({html.escape(error_type)}):</b>\n<pre>{html.escape(error_msg[:500])}</pre>\n\n"
            detailed_error += f"<b>Fallback Error ({html.escape(error_type2)}):</b>\n<pre>{html.escape(error_msg2[:500])}</pre>\n\n"
            detailed_error += f"<i>Please check your API key, quota, and internet connection.</i>"
            return detailed_error


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
            
            # Extract user's first name
            first_name = update.message.from_user.first_name
            # Optional: Get last name if available
            last_name = update.message.from_user.last_name if update.message.from_user.last_name else ""
            
            # Construct full name, prioritizing first name
            user_full_name = f"{first_name} {last_name}".strip() if first_name else f"User {user_id}"
            
            print(f"✅ Message received!")
            print(f"   Chat ID: {chat_id}")
            print(f"   User ID: {user_id}")
            print(f"   User Name: {user_full_name}")
            print(f"   Message: {user_message}")
            
            if not user_message:
                print("⚠️  Message text is empty")
                return "OK", 200
            
            # Prepend user's name to the message for personalization
            personalized_message = f"Hello {user_full_name}, you asked: {user_message}"
            
            # Get Gemini response
            print("Calling Gemini API...")
            response_text = get_gemini_response(personalized_message)
            print(f"✅ Gemini response received")
            print(f"   Response: {response_text[:200]}")
            
            # ⭐️ NEW STEP: Chunk the response
            response_chunks = chunk_response_for_telegram(response_text)
            
            # Send response (Iterate through chunks)
            print(f"Sending {len(response_chunks)} message(s) to Telegram...")
            if bot:
                for chunk in response_chunks:
                    # Using parse_mode='HTML' as recommended
                    bot.send_message(chat_id, chunk, parse_mode='HTML')
                    # Note: telebot handles the necessary delays between messages.

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
            
            # Extract user's first name
            first_name = message.from_user.first_name
            # Optional: Get last name if available
            last_name = message.from_user.last_name if message.from_user.last_name else ""
            
            # Construct full name, prioritizing first name
            user_full_name = f"{first_name} {last_name}".strip() if first_name else f"User {message.from_user.id}"
            
            print(f"Polling received message from {chat_id} ({user_full_name}): {user_message[:50]}")
            
            # Prepend user's name to the message for personalization
            personalized_message = f"Hello {user_full_name}, you asked: {user_message}"
            
            # Get Gemini response
            response_text = get_gemini_response(personalized_message)
            print(f"Response: {response_text[:100]}")
            
            # ⭐️ NEW STEP: Chunk the response
            response_chunks = chunk_response_for_telegram(response_text)
            
            # Send response (Iterate through chunks)
            for chunk in response_chunks:
                # Using parse_mode='HTML' as recommended
                bot.send_message(chat_id, chunk, parse_mode='HTML')

        except Exception as e:
            print(f"Error handling message: {e}")
            bot.send_message(message.chat.id, f"Error: {str(e)}", parse_mode='HTML')
    
    print("Starting polling mode...")
    bot.infinity_polling(timeout=30)

