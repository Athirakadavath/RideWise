from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.database import get_db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)


def get_user_id(cursor, username):
    user = cursor.execute(
        "SELECT id FROM users WHERE username = ? ",
        (username,)
    ).fetchone()
    return user["id"] if user else None


@dashboard_bp.route('/stats', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_dashboard_stats():
    if request.method == 'OPTIONS':
        from flask import request
        return jsonify({"status": "ok"}), 200

    try:
        username = get_jwt_identity()

        conn = get_db()
        cursor = conn.cursor()

        user_id = get_user_id(cursor, username)
        if not user_id:
            conn.close()
            return jsonify({"error": "User not found"}), 404

        # Total predictions
        total_predictions = cursor.execute(
            'SELECT COUNT(*) as count FROM predictions WHERE user_id = ?',
            (user_id,)
        ).fetchone()['count']

        # Daily predictions count
        daily_count = cursor.execute(
            'SELECT COUNT(*) as count FROM predictions WHERE user_id = ? AND prediction_type = "daily"',
            (user_id,)
        ).fetchone()['count']

        # Hourly predictions count
        hourly_count = cursor.execute(
            'SELECT COUNT(*) as count FROM predictions WHERE user_id = ? AND prediction_type = "hourly"',
            (user_id,)
        ).fetchone()['count']

        # Last prediction
        last_prediction = cursor.execute(
            '''SELECT prediction_value, prediction_type, created_at
               FROM predictions
               WHERE user_id = ?
               ORDER BY created_at DESC
               LIMIT 1''',
            (user_id,)
        ).fetchone()

        # Feedback count
        feedback_count = cursor.execute(
            'SELECT COUNT(*) as count FROM feedback WHERE user_id = ?',
            (user_id,)
        ).fetchone()['count']

        conn.close()

        # Format last prediction
        last_pred_text = "--"
        if last_prediction:
            pred_date = datetime.fromisoformat(last_prediction['created_at'])
            last_pred_text = pred_date.strftime("%b %d, %Y")

        return jsonify({
            "success": True,
            "stats": {
                "total_predictions": total_predictions,
                "daily_predictions": daily_count,
                "hourly_predictions": hourly_count,
                "last_prediction": last_pred_text,
                "last_prediction_value": last_prediction['prediction_value'] if last_prediction else None,
                "last_prediction_type": last_prediction['prediction_type'] if last_prediction else None,
                "feedback_count": feedback_count,
                "accuracy_rate": 95  # You can calculate this based on actual vs predicted if you have that data
            }
        }), 200

    except Exception as e:
        print(f"❌ Dashboard stats error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to load statistics"}), 500