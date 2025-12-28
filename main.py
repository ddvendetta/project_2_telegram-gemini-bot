import os
import time
import json
import html
import telebot
from collections import deque
import google.genai as genai
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
# Use GOOGLE_API_KEY as it's the standard env var name and what the deploy script sets
gemini_api_key = os.environ.get("GOOGLE_API_KEY")

print(f"Initializing bot with token: {tg_token[:20] if tg_token else 'MISSING'}...")
print(f"Initializing Gemini with key: {gemini_api_key[:20] if gemini_api_key else 'MISSING'}...")
print(f"Running in GCF mode: {IS_GCF}")

try:
    bot = telebot.TeleBot(tg_token, parse_mode='HTML') if tg_token else None
    if gemini_api_key:
        print("Gemini API key found.")

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

# Rate limiting: Gemini Free Tier is typically 15 RPM (Requests Per Minute)
GEMINI_RPM_LIMIT = 15
# WARNING: This in-memory rate limiter is not suitable for production.
# In a serverless environment, each instance will have its own rate limiter,
# making the global limit ineffective. A persistent store like Redis or
# Firestore is required for a robust implementation.
global_request_timestamps = deque()


# Define the hard character limit for each chunk (Keep this around 700-4000)
MAX_CHUNK_LIMIT = 3000

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

def get_gemini_response(chat_id, user_message):
    """Get response from Gemini with Google Search grounding."""
    try:
        print(f"get_gemini_response called for {chat_id} with: {user_message[:100]}")

        # --- In-memory Rate Limit Check ---
        current_time = time.time()
        while global_request_timestamps and global_request_timestamps[0] < current_time - 60:
            global_request_timestamps.popleft()
            
        if len(global_request_timestamps) >= GEMINI_RPM_LIMIT:
            print(f"⚠️ Rate limit hit: {len(global_request_timestamps)} requests in last 60s")
            return "<b>⚠️ System Busy</b>\n\nI'm receiving too many messages right now (Free Tier Limit: 15/min). Please try again in a few seconds."
        
        global_request_timestamps.append(current_time)
        # ------------------------------------

        enhanced_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"

        # This is the stable configuration that was proven to work.
        # It relies on the model's automatic grounding capabilities.
        client = genai.Client(api_key=gemini_api_key)
        
        print("Calling generate_content (automatic grounding)...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=enhanced_prompt,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ]
            )
        )
        
        full_response = response.text if hasattr(response, 'text') else ""
        print(f"Full response received: {len(full_response)} chars")
        
        result = full_response if full_response else "No response generated"
        
        return result

    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"❌ Gemini error: {error_type}: {error_msg}")
        import traceback
        traceback.print_exc()
        # Return detailed error information with HTML escaping
        detailed_error = f"<b>❌ Gemini API Error</b>\n\n"
        detailed_error += f"<b>Error Type:</b> <pre>{html.escape(error_type)}</pre>\n"
        detailed_error += f"<b>Message:</b> <pre>{html.escape(error_msg[:1000])}</pre>\n\n"
        detailed_error += f"<i>Please check your API key, quota, and the service status.</i>"
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
            print(f"Request JSON: {json.dumps(request_json, indent=2)}")
            
            if not request_json:
                print("⚠️  Empty request body")
                return "OK", 200
            
            update = telebot.types.Update.de_json(request_json)
            
            if not update.message or not update.message.text:
                print("⚠️  No message or text in update")
                return "OK", 200
            
            user_message = update.message.text
            chat_id = update.message.chat.id
            user_id = update.message.from_user.id
            first_name = update.message.from_user.first_name
            last_name = update.message.from_user.last_name or ""
            user_full_name = f"{first_name} {last_name}".strip() or f"User {user_id}"
            
            print(f"✅ Message received!")
            print(f"   Chat ID: {chat_id}")
            print(f"   User: {user_full_name}")
            print(f"   Message: {user_message}")
            
            # Get Gemini response
            print("Calling Gemini API...")
            response_text = get_gemini_response(chat_id, user_message)
            print(f"✅ Gemini response received (first 200 chars): {response_text[:200]}")
            
            response_chunks = chunk_response_for_telegram(response_text)
            
            print(f"Sending {len(response_chunks)} message(s) to Telegram...")
            if bot:
                for i, chunk in enumerate(response_chunks):
                    bot.send_message(chat_id, chunk, parse_mode='HTML')
                    print(f"   Sent chunk {i+1}/{len(response_chunks)}")

                print("✅ All message chunks sent successfully!")
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
    if bot:
        @bot.message_handler(func=lambda message: True)
        def handle_message(message):
            """Handle incoming messages in polling mode"""
            try:
                user_message = message.text
                chat_id = message.chat.id
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name or ""
                user_full_name = f"{first_name} {last_name}".strip() or f"User {message.from_user.id}"
                
                print(f"Polling received message from {chat_id} ({user_full_name}): {user_message[:50]}")
                
                # Get Gemini response
                response_text = get_gemini_response(chat_id, user_message)
                print(f"Response (first 100 chars): {response_text[:100]}")
                
                response_chunks = chunk_response_for_telegram(response_text)
                
                for chunk in response_chunks:
                    bot.send_message(chat_id, chunk, parse_mode='HTML')

            except Exception as e:
                print(f"Error handling message: {e}")
                bot.send_message(message.chat.id, f"Error: {str(e)}", parse_mode='HTML')
        
        print("Starting polling mode...")
        bot.infinity_polling(timeout=30)
    else:
        print("❌ Bot not initialized. Please check your TG_KEY environment variable.")
