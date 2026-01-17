from flask import Blueprint, request, jsonify
from utils.database import get_db

chatbot_bp = Blueprint("chatbot", __name__)


def generate_response(message):
    """Enhanced rule-based response system"""
    message_lower = message.lower()

    # Greetings
    if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "👋 Hello!  I'm your RideWise AI Assistant. I can help you with:\n• Making bike demand predictions 📊\n• Understanding weather impact 🌤️\n• Finding peak rental hours ⏰\n• Navigating the platform\n\nWhat would you like to know?"

    # Peak hours
    if any(word in message_lower for word in ["peak", "busy", "hour", "time"]):
        return "⏰ Peak rental hours:\n\n🌅 Morning Rush:  7-9 AM (commuters)\n🌆 Evening Rush: 5-7 PM (commuters)\n📅 Weekends: 12-4 PM (leisure)\n\nWant to predict demand for a specific hour?"

    # Weather
    if "weather" in message_lower:
        return "🌤️ Weather has a HUGE impact on bike rentals!\n\n☀️ Clear days:  Highest demand (+50-75%)\n🌥️ Cloudy/Mist: Moderate demand\n🌧️ Light rain: Lower demand (-30%)\n⛈️ Heavy rain/storms: Lowest demand (-60%)\n\nWant to make a weather-based prediction?"

    # Predictions
    if any(word in message_lower for word in ["predict", "prediction", "forecast"]):
        return "📊 Here's how to make predictions:\n\n1️⃣ Go to 'Predict Demand'\n2️⃣ Choose type (Daily or Hourly)\n3️⃣ Enter date and weather conditions\n4️⃣ Get AI-powered forecast!\n\n💡 Tip: You can also upload a PDF!"

    # How it works
    if "how" in message_lower:
        return "🎯 RideWise uses machine learning to predict bike demand!\n\nWe analyze:\n• Historical rental patterns\n• Weather conditions 🌤️\n• Day/time factors ⏰\n• Seasonal trends 🍂\n\nWant to try making a prediction?"

    # Help
    if "help" in message_lower:
        return "🆘 I'm here to help!  Ask me about:\n\n📊 Making predictions\n🌤️ Weather impact\n⏰ Peak hours\n🗺️ Finding stations\n📈 Analytics\n\nWhat do you need help with?"

    # Thank you
    if "thank" in message_lower:
        return "You're welcome! 😊 Feel free to ask anything else!"

    # Default
    return "I'm your RideWise AI Assistant! 🤖\n\nI can help with:\n• Making predictions 📊\n• Weather impact 🌤️\n• Peak hours ⏰\n• Finding stations 🗺️\n• Analytics 📈\n\nWhat would you like to know?"


@chatbot_bp.route("/message", methods=["POST", "OPTIONS"])
def chatbot_message():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    print("\n" + "="*50)
    print("🔵 CHATBOT MESSAGE RECEIVED")
    print("="*50)

    try:
        data = request.get_json()
        print(f"📦 Data:  {data}")

        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        message = data.get("message", "").strip()
        print(f"📩 Message: '{message}'")

        if not message:
            return jsonify({"success":  False, "error": "Message cannot be empty"}), 400

        # Generate response
        response = generate_response(message)
        print(f"🤖 Response: {response[: 100]}...")

        print("✅ Success!")
        print("="*50 + "\n")

        return jsonify({"success": True, "response": response}), 200

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("="*50 + "\n")
        return jsonify({"success": False, "error": str(e)}), 500


@chatbot_bp.route("/history", methods=["GET", "OPTIONS"])
def chatbot_history():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    # Return empty history for now
    return jsonify({"success": True, "history": []}), 200