from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from utils.database import get_db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json()

        # Validate input
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data. get('password', '')

        if not username or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        if len(username) < 3:
            return jsonify({"error": "Username must be at least 3 characters"}), 400

        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        # Database operations
        conn = get_db()
        cursor = conn.cursor()

        # Check if username exists
        existing_user = cursor.execute(
            'SELECT id FROM users WHERE username = ? ',
            (username,)
        ).fetchone()

        if existing_user:
            conn. close()
            return jsonify({"error": "Username already exists"}), 409

        # Check if email exists
        existing_email = cursor.execute(
            'SELECT id FROM users WHERE email = ?',
            (email,)
        ).fetchone()

        if existing_email:
            conn.close()
            return jsonify({"error":  "Email already registered"}), 409

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insert new user
        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, hashed_password)
        )

        conn.commit()
        user_id = cursor.lastrowid
        conn. close()

        # Create JWT token
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(days=7)
        )

        print(f"✅ User registered:  {username}")

        return jsonify({
            "success": True,
            "message": "Registration successful",
            "token": access_token,
            "user": {
                "id": user_id,
                "username": username,
                "email": email
            }
        }), 201

    except Exception as e:
        print(f"❌ Registration error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Registration failed.  Please try again."}), 500


@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json()

        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        conn = get_db()
        cursor = conn. cursor()

        user = cursor. execute(
            'SELECT id, username, email, password FROM users WHERE username = ?',
            (username,)
        ).fetchone()

        conn.close()

        if not user:
            return jsonify({"error": "Invalid username or password"}), 401

        if not check_password_hash(user['password'], password):
            return jsonify({"error": "Invalid username or password"}), 401

        # Create JWT token
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(days=7)
        )

        print(f"✅ User logged in: {username}")

        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": access_token,
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email']
            }
        }), 200

    except Exception as e:
        print(f"❌ Login error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Login failed. Please try again."}), 500


@auth_bp. route('/verify', methods=['GET', 'OPTIONS'])
@jwt_required()
def verify():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        current_user = get_jwt_identity()

        conn = get_db()
        cursor = conn.cursor()

        user = cursor.execute(
            'SELECT id, username, email FROM users WHERE username = ? ',
            (current_user,)
        ).fetchone()

        conn.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "success": True,
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email']
            }
        }), 200

    except Exception as e:
        print(f"❌ Verify error: {e}")
        return jsonify({"error": "Verification failed"}), 500