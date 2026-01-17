from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from utils.database import get_db

chatbot_bp = Blueprint("chatbot", __name__)


def safe_error(message="Something went wrong"):
    return jsonify({"success": False, "error": message}), 400


def get_user_id(cursor, username):
    user = cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    return user["id"] if user else None


def generate_response(message, context=""):
    """Enhanced rule-based response system"""
    message_lower = message.lower()

    # Greetings
    if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "👋 Hello! I'm your RideWise AI Assistant.  I can help you with:\n• Making bike demand predictions 📊\n• Understanding weather impact 🌤️\n• Finding peak rental hours ⏰\n• Navigating the platform\n\nWhat would you like to know?"

    # Peak hours / busy times
    if any(word in message_lower for word in ["peak", "busy", "hour", "time", "when"]):
        if "weekend" in message_lower:
            return "📅 Weekend peak hours:\n• 10 AM - 4 PM (Leisure riders)\n• Especially busy:  12 PM - 2 PM\n\nWeekends see more leisure trips vs weekday commutes!"
        else:
            return "⏰ Peak rental hours:\n\n🌅 Morning Rush:  7-9 AM (commuters)\n🌆 Evening Rush: 5-7 PM (commuters)\n📅 Weekends: 12-4 PM (leisure)\n\nWant to predict demand for a specific hour?"

    # Weather-related
    if "weather" in message_lower:
        return "🌤️ Weather has a HUGE impact on bike rentals!\n\n☀️ Clear days:  Highest demand (+50-75%)\n🌥️ Cloudy/Mist: Moderate demand\n🌧️ Light rain: Lower demand (-30%)\n⛈️ Heavy rain/storms: Lowest demand (-60%)\n\nWant to make a weather-based prediction?"

    # Predictions
    if any(word in message_lower for word in ["predict", "prediction", "forecast"]):
        return "📊 Here's how to make predictions:\n\n1️⃣ Go to 'Predict Demand'\n2️⃣ Choose type (Daily or Hourly)\n3️⃣ Enter date and weather conditions\n4️⃣ Get AI-powered forecast!\n\n💡 Tip: You can also upload a PDF with parameters!"

    # How it works
    if "how" in message_lower and ("work" in message_lower or "use" in message_lower):
        return "🎯 RideWise uses machine learning to predict bike demand!\n\nWe analyze:\n• Historical rental patterns\n• Weather conditions 🌤️\n• Day/time factors ⏰\n• Seasonal trends 🍂\n\nOur XGBoost model achieves 95% accuracy!  Want to try making a prediction?"

    # Stations / Map
    if any(word in message_lower for word in ["station", "map", "location", "where", "find"]):
        return "🗺️ Check out our Bike Stations map to find rental locations near you!  Click 'Bike Stations' in the menu to:\n• View all station locations\n• See real-time availability\n• Plan your trip"

    # Help
    if "help" in message_lower:
        return "🆘 I'm here to help!  Ask me about:\n\n📊 Making predictions\n🌤️ Weather impact\n⏰ Peak hours\n🗺️ Finding stations\n📈 Analytics\n❓ How RideWise works\n\nWhat do you need help with?"

    # Thank you
    if "thank" in message_lower:
        return "You're welcome! 😊 Feel free to ask anything else about bike demand predictions!"

    # Default response
    return "I'm your RideWise AI Assistant!  🤖\n\nI can help with:\n• Making bike demand predictions 📊\n• Understanding weather impact 🌤️\n• Finding peak rental hours ⏰\n• Exploring bike stations 🗺️\n• Viewing analytics 📈\n\nWhat would you like to know?"


@chatbot_bp.route("/message", methods=["POST", "OPTIONS"])
def chatbot_message():
    if request.method == "OPTIONS":
        return jsonify({"status":  "ok"}), 200

    print("\n" + "="*50)
    print("🔵 CHATBOT MESSAGE ENDPOINT HIT")
    print("="*50)

    try:
        # Check Authorization header
        auth_header = request.headers.get('Authorization')
        print(f"🔑 Authorization header: {auth_header[: 50] if auth_header else 'MISSING'}...")

        # Verify JWT manually first
        try:
            verify_jwt_in_request()
            username = get_jwt_identity()
            print(f"✅ JWT verified, username: {username}")
        except Exception as jwt_error:
            print(f"❌ JWT verification failed:  {jwt_error}")
            return jsonify({"success": False, "error": "Authentication failed.  Please log in again."}), 401

        # Get request data
        data = request.get_json()
        print(f"📦 Request data: {data}")

        if not data:
            print("❌ No JSON data received")
            return safe_error("No data provided")

        message = data.get("message", "").strip()
        print(f"📩 Message: '{message}'")

        if not message:
            print("❌ Empty message")
            return safe_error("Message cannot be empty")

        # Database operations
        try:
            conn = get_db()
            cursor = conn.cursor()
            print("✅ Database connection established")
        except Exception as db_error:
            print(f"❌ Database connection failed: {db_error}")
            return safe_error("Database connection failed")

        # Get user ID
        user_id = get_user_id(cursor, username)
        print(f"👤 User ID: {user_id}")

        if not user_id:
            conn.close()
            print("❌ User not found in database")
            return safe_error("User not found")

        # Generate response
        response = generate_response(message)
        print(f"🤖 Generated response: {response[: 100]}...")

        # Save to database
        try:
            cursor.execute(
                """
                INSERT INTO chat_history (user_id, message, response, source)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, message, response, "text")
            )
            conn.commit()
            print("✅ Chat saved to database")
        except Exception as save_error:
            print(f"❌ Failed to save chat: {save_error}")
            conn.close()
            return safe_error("Failed to save message")

        conn.close()

        print("✅ Success!  Returning response")
        print("="*50 + "\n")

        return jsonify({"success":  True, "response": response}), 200

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("="*50 + "\n")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@chatbot_bp.route("/history", methods=["GET", "OPTIONS"])
def chatbot_history():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        # Verify JWT
        verify_jwt_in_request()
        username = get_jwt_identity()

        limit = int(request.args.get("limit", 20))

        conn = get_db()
        cursor = conn.cursor()

        user_id = get_user_id(cursor, username)

        if not user_id:
            conn.close()
            return safe_error("User not found")

        rows = cursor.execute(
            """
            SELECT message, response, source, created_at
            FROM chat_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit)
        ).fetchall()

        conn.close()

        history = [{
            "message": r["message"],
            "response": r["response"],
            "source":  r["source"],
            "created_at": r["created_at"]
        } for r in rows]

        return jsonify({"success": True, "history": history}), 200

    except Exception as e:
        print(f"❌ History error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": "Failed to load history"}), 500