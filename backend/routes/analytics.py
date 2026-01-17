from flask import Blueprint, request, jsonify
from utils.database import get_db
import jwt
from config import Config

analytics_bp = Blueprint('analytics', __name__)

def get_user_id():
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        return None
    try:
        token = auth.split(' ')[1]
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id')
    except:
        return None


@analytics_bp.route('/weather-impact', methods=['GET'])
def weather_impact():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"weather_impact": []}), 200

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            CASE
                WHEN input_data LIKE '%weathersit%1%' THEN 'Clear'
                WHEN input_data LIKE '%weathersit%2%' THEN 'Cloudy'
                WHEN input_data LIKE '%weathersit%3%' THEN 'Rainy'
                WHEN input_data LIKE '%weathersit%4%' THEN 'Stormy'
                ELSE 'Unknown'
            END AS weather,
            AVG(prediction_value) AS avg_prediction,
            COUNT(*) AS count
        FROM predictions
        WHERE user_id = ?
        GROUP BY weather
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return jsonify({
        "weather_impact": [
            {
                "weather": r["weather"],
                "avg_prediction": round(r["avg_prediction"], 2),
                "count": r["count"]
            }
            for r in rows if r["weather"] != "Unknown"
        ]
    }), 200

@analytics_bp.route('/hourly-patterns', methods=['GET'])
def hourly_patterns():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"hourly_patterns": []}), 200

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            CAST(SUBSTR(input_data, INSTR(input_data, 'hr') + 2, 2) AS INTEGER) AS hour,
            AVG(prediction_value) AS avg_prediction,
            COUNT(*) AS count
        FROM predictions
        WHERE user_id = ?
          AND prediction_type = 'hourly'
          AND input_data LIKE '%hr%'
        GROUP BY hour
        ORDER BY hour
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return jsonify({
        "hourly_patterns": [
            {
                "hour": r["hour"],
                "avg_prediction": round(r["avg_prediction"], 2),
                "count": r["count"]
            }
            for r in rows if r["hour"] is not None and 0 <= r["hour"] <= 23
        ]
    }), 200
