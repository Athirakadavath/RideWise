import google.generativeai as genai
from config import Config

# Configure Gemini
genai.configure(api_key=Config. GEMINI_API_KEY)

# System context about RideWise
RIDEWISE_CONTEXT = """
You are RideWise AI Assistant, a helpful chatbot for a bike-sharing demand prediction platform.

**About RideWise:**
- RideWise is an AI-powered bike-sharing demand prediction system
- It helps predict daily and hourly bike rental demand
- Users can make predictions based on weather, date, and time
- The system analyzes historical data to forecast demand

**Key Features:**
1. **Daily Predictions**: Forecast total bike demand for a specific day
2. **Hourly Predictions**: Predict demand for specific hours (0-23)
3. **Weather Impact**: Weather significantly affects rentals (clear > cloudy > rainy)
4. **Peak Hours**:
   - Morning rush:  7-9 AM (commuters)
   - Evening rush: 5-7 PM (commuters)
   - Weekend peaks: 12-4 PM (leisure riders)
5. **PDF Upload**: Users can upload PDFs with prediction parameters
6. **Analytics Dashboard**: View trends, weather impact, hourly patterns
7. **Station Map**: Explore bike station locations

**Weather Impact:**
- Weather situation codes:
  - 1 = Clear/Partly Cloudy (☀️) → Highest demand
  - 2 = Mist/Cloudy (🌥️) → Moderate demand
  - 3 = Light Rain/Snow (🌧️) → Lower demand
  - 4 = Heavy Rain/Storms (⛈️) → Lowest demand

**Seasons:**
- Spring (Mar-May): Moderate demand, increasing
- Summer (Jun-Aug): Highest demand
- Fall (Sep-Nov): Moderate demand, decreasing
- Winter (Dec-Feb): Lowest demand

**User Help:**
- Guide users on how to make predictions
- Explain weather parameters (temperature, humidity, wind speed normalized 0-1)
- Suggest best times for bike rentals
- Provide insights on demand patterns

**Tone:** Friendly, helpful, and informative.  Use emojis occasionally.  Keep responses concise but informative.
"""


def generate_ai_response(user_message, chat_history=None):
    """
    Generate intelligent response using Gemini AI

    Args:
        user_message: User's current message
        chat_history: Previous conversation context (optional)

    Returns:
        AI-generated response string
    """

    try:
        # Create the model
        model = genai. GenerativeModel('gemini-pro')

        # Build conversation context
        conversation = RIDEWISE_CONTEXT + "\n\n"

        if chat_history:
            conversation += "**Previous Conversation:**\n"
            for msg in chat_history[-5:]:  # Last 5 messages for context
                conversation += f"User: {msg['message']}\n"
                conversation += f"Assistant: {msg['response']}\n"
            conversation += "\n"

        conversation += f"**Current User Message:** {user_message}\n\n"
        conversation += "**Your Response:**"

        # Generate response
        response = model.generate_content(conversation)

        return response. text. strip()

    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fallback to rule-based response
        return generate_fallback_response(user_message)


def generate_fallback_response(message):
    """
    Simple rule-based fallback if Gemini fails
    """
    message_lower = message.lower()

    if "weather" in message_lower:
        return "🌤️ Weather significantly impacts bike rentals!  Clear days see 50-75% more rentals than rainy days.  Would you like to make a weather-based prediction?"

    if "peak" in message_lower or "busy" in message_lower or "hour" in message_lower:
        return "⏰ Peak rental hours are:\n• Morning: 7-9 AM (commuters 🚴‍♂️)\n• Evening: 5-7 PM (commuters)\n• Weekends: 12-4 PM (leisure riders)\n\nWant to predict demand for a specific hour?"

    if "predict" in message_lower or "forecast" in message_lower:
        return "📊 I can help you make predictions!  You can:\n1. Make a Daily prediction (total demand)\n2. Make an Hourly prediction (specific time)\n3. Upload a PDF with parameters\n\nWhich would you like to try?"

    if "how" in message_lower and ("work" in message_lower or "use" in message_lower):
        return "🎯 Here's how RideWise works:\n1. Go to 'Predict Demand' 📈\n2. Choose prediction type (Daily/Hourly)\n3. Enter date, weather, and conditions\n4. Get AI-powered demand forecast!\n\nYou can also view Analytics 📊 and explore Bike Stations 🗺️."

    if "station" in message_lower or "map" in message_lower or "location" in message_lower:
        return "🗺️ Check out our Bike Stations map to find rental locations near you!  You can view real-time availability and plan your trip."

    if "hello" in message_lower or "hi" in message_lower or "hey" in message_lower:
        return "👋 Hello! I'm your RideWise AI Assistant. I can help you with:\n• Making demand predictions 📊\n• Understanding weather impact 🌤️\n• Finding peak hours ⏰\n• Navigating the platform\n\nWhat would you like to know?"

    if "thank" in message_lower:
        return "You're welcome! 😊 Feel free to ask if you need anything else!"

    return "I'm here to help with bike demand predictions!  You can ask me about:\n• Making predictions 📊\n• Weather impact 🌤️\n• Peak rental hours ⏰\n• How to use RideWise\n\nWhat would you like to know?"


def get_chat_history_for_context(cursor, user_id, limit=5):
    """
    Get recent chat history for context
    """
    rows = cursor.execute(
        """
        SELECT message, response
        FROM chat_history
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (user_id, limit)
    ).fetchall()

    return [{"message": r["message"], "response": r["response"]} for r in reversed(rows)]