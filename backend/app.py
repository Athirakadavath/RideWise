from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from utils.database import init_db
import os

# Import blueprints
from routes.auth import auth_bp
from routes. predictions import predictions_bp
from routes. analytics import analytics_bp
from routes. stations import stations_bp
from routes.chatbot import chatbot_bp
from routes.dashboard import dashboard_bp  # ✅ Add this

app = Flask(__name__)
app.config.from_object(Config)

# Initialize JWT
jwt = JWTManager(app)

# Enhanced CORS Configuration
CORS(app,
     resources={r"/api/*": {
         "origins": Config.CORS_ORIGINS,
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
         "supports_credentials": True,
         "expose_headers": ["Content-Type", "Authorization"]
     }},
     supports_credentials=True
)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(predictions_bp, url_prefix='/api/predictions')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(stations_bp, url_prefix='/api/stations')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')  # ✅ Add this

# Add explicit OPTIONS handler
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 200

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "message": "RideWise API is running"}), 200

# Test CORS endpoint
@app.route('/api/test', methods=['GET', 'POST', 'OPTIONS'])
def test():
    return jsonify({"message": "CORS is working!", "origin": request.headers.get("Origin")}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('models', exist_ok=True)

    # Initialize database
    print("🔄 Initializing database...")
    init_db()

    # Run the app
    print("🚀 Starting RideWise API server...")
    print(f"✅ CORS enabled for:  {Config.CORS_ORIGINS}")
    app.run(
        debug=Config.DEBUG,
        host='0.0.0.0',
        port=5000
    )