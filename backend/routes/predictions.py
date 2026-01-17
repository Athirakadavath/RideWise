from flask import Blueprint, request, jsonify
from models.ml_model import predict_daily, predict_hourly
from services. pdf_parser import extract_data_from_pdf
from utils.database import get_db
import jwt
from config import Config
import os

predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/daily', methods=['POST', 'OPTIONS'])
def predict_daily_route():
    """Daily bike demand prediction"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields
        required_fields = ['date', 'season', 'yr', 'mnth', 'weekday', 'holiday',
                          'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed']

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Make prediction
        prediction = predict_daily(data)

        # Get user ID and save prediction (optional)
        user_id = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
            except:
                pass

        if user_id:
            try:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO predictions (user_id, prediction_type, input_data, prediction_value)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, 'daily', str(data), int(prediction)))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Error saving prediction: {e}")

        return jsonify({
            "success": True,
            "prediction":  int(prediction),
            "type": "daily",
            "message": f"Predicted daily bike demand: {int(prediction)} bikes"
        }), 200

    except Exception as e:
        print(f"Daily prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@predictions_bp.route('/hourly', methods=['POST', 'OPTIONS'])
def predict_hourly_route():
    """Hourly bike demand prediction"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields
        required_fields = ['date', 'season', 'yr', 'mnth', 'weekday', 'holiday',
                          'workingday', 'weathersit', 'temp', 'atemp', 'hum',
                          'windspeed', 'hr']

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Make prediction
        prediction = predict_hourly(data)

        # Save prediction (optional)
        user_id = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, Config. SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
            except:
                pass

        if user_id:
            try:
                conn = get_db()
                cursor = conn.cursor()
                cursor. execute('''
                    INSERT INTO predictions (user_id, prediction_type, input_data, prediction_value)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, 'hourly', str(data), int(prediction)))
                conn. commit()
                conn.close()
            except Exception as e:
                print(f"Error saving prediction: {e}")

        return jsonify({
            "success": True,
            "prediction":  int(prediction),
            "type": "hourly",
            "message": f"Predicted hourly bike demand: {int(prediction)} bikes"
        }), 200

    except Exception as e:
        print(f"Hourly prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@predictions_bp.route('/upload-pdf', methods=['POST', 'OPTIONS'])
def upload_pdf():
    """Handle PDF upload and extract prediction data"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        if 'file' not in request. files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        prediction_type = request.form.get('type', 'daily')

        if file.filename == '':
            return jsonify({"error":  "No file selected"}), 400

        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Only PDF files are allowed"}), 400

        # Create upload folder if it doesn't exist
        upload_folder = Config.UPLOAD_FOLDER
        os.makedirs(upload_folder, exist_ok=True)

        # Save uploaded file temporarily
        file_path = os. path.join(upload_folder, file.filename)
        file.save(file_path)

        print(f"PDF saved to: {file_path}")

        # Extract data from PDF
        extracted_data = extract_data_from_pdf(file_path)

        if not extracted_data:
            os.remove(file_path)
            return jsonify({"error":  "Could not extract data from PDF.  Please ensure the PDF contains the required fields."}), 400

        # Make prediction based on type
        try:
            if prediction_type == 'daily':
                prediction = predict_daily(extracted_data)
            else:
                # For hourly, ensure 'hr' is present
                if 'hr' not in extracted_data:
                    extracted_data['hr'] = 12  # Default to noon
                prediction = predict_hourly(extracted_data)
        except Exception as pred_error:
            os.remove(file_path)
            return jsonify({"error": f"Prediction failed: {str(pred_error)}"}), 500

        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass

        return jsonify({
            "success": True,
            "prediction": int(prediction),
            "type": prediction_type,
            "extracted_data": extracted_data,
            "message": f"PDF processed successfully.  Predicted {int(prediction)} bikes."
        }), 200

    except Exception as e:
        print(f"PDF upload error: {str(e)}")
        # Try to clean up file if it exists
        try:
            if 'file_path' in locals():
                os.remove(file_path)
        except:
            pass
        return jsonify({"error": f"PDF processing failed: {str(e)}"}), 500


@predictions_bp.route('/history', methods=['GET', 'OPTIONS'])
def get_prediction_history():
    """Get user's prediction history"""
    if request.method == 'OPTIONS':
        return '', 200

    try:
        # Get user ID from token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error":  "No token provided"}), 401

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
        except:
            return jsonify({"error": "Invalid token"}), 401

        # Get predictions from database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, prediction_type, prediction_value, created_at
            FROM predictions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 20
        ''', (user_id,))

        predictions = cursor.fetchall()
        conn.close()

        history = []
        for pred in predictions:
            history.append({
                'id': pred['id'],
                'type': pred['prediction_type'],
                'value': pred['prediction_value'],
                'createdAt': pred['created_at']
            })

        return jsonify({
            "success": True,
            "predictions": history
        }), 200

    except Exception as e:
        print(f"History error: {str(e)}")
        return jsonify({"error": str(e)}), 500