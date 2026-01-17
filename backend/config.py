import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # Flask
    SECRET_KEY = os. getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/ridewise.db')

    # Models
    DAILY_MODEL_PATH = os.getenv('DAILY_MODEL_PATH', 'models/xgb_day_new.pkl')
    HOURLY_MODEL_PATH = os. getenv('HOURLY_MODEL_PATH', 'models/xgb_hour_new.pkl')

    # File Upload
    UPLOAD_FOLDER = 'uploads'
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'pdf'}

    # Google Maps
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

    # Gemini AI (Chatbot)
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

    # Bike Stations
    STATIONS_DATA_PATH = 'data/bike_stations.json'

    # CORS - ✅ Added port 3002
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:3002',  # ✅ Added this
        'http://127.0.0.1:3002',  # ✅ Added this
        'http://localhost:5173'
    ]