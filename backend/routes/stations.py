from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.database import get_db

stations_bp = Blueprint('stations', __name__)  # ← Make sure this line exists!

@stations_bp.route('/nearby', methods=['POST'])
@jwt_required()
def get_nearby():
    """Get nearby bike stations"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        radius = data.get('radius', 5000)
        city = data.get('city', 'capital')

        if not latitude or not longitude:
            return jsonify({'error': 'Latitude and longitude are required'}), 400

        nearby_stations = get_nearby_stations(latitude, longitude, radius, city)

        return jsonify({'success': True, 'stations': nearby_stations, 'count': len(nearby_stations)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stations_bp.route('/all', methods=['GET'])
def get_all():
    """Get all bike stations"""
    try:
        city = request.args.get('city', 'capital')
        stations = get_all_stations(city)

        return jsonify({'success': True, 'stations': stations, 'count': len(stations)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stations_bp.route('/<station_id>', methods=['GET'])
def get_station(station_id):
    """Get station details"""
    try:
        city = request.args.get('city', 'capital')
        station = get_station_details(station_id, city)

        if not station:
            return jsonify({'error': 'Station not found'}), 404

        return jsonify({'success':  True, 'station': station}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500